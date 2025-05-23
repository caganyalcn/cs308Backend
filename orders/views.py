from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from products.models import Cart, CartItem, Product
from .utils import generate_invoice_pdf
from accounts.models import User
from django.views.decorators.http import require_POST, require_GET, require_http_methods
import json
import os

from django.core.mail import EmailMessage
from django.conf import settings

from .serializers import OrderSerializer
from datetime import datetime

def send_invoice_email(user_email, pdf_path):
    subject = 'Order Invoice - ÇiftlikBank'
    body = 'Your order has been completed successfully. The invoice is attached.'

    email = EmailMessage(subject, body, to=[user_email])
    email.attach_file(pdf_path)
    email.send()

def send_cancellation_email(user_email, order_id, order_items, total_price):
    subject = f'Order #{order_id} Cancelled - ÇiftlikBank'
    message_body = f"Merhaba,\n\nSiparişiniz #{order_id} başarıyla iptal edilmiştir.\n\nİptal Edilen Ürünler:\n"
    for item in order_items:
        message_body += f"- {item['name']} ({item['quantity']} adet) - Fiyat: {item['price']:.2f} TL\n"
    message_body += f"\nToplam Tutar: {total_price:.2f} TL\n"
    message_body += "\nTeşekkür ederiz.\nÇiftlikBank Ekibiniz"

    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message_body, from_email, [user_email], fail_silently=False)

@csrf_exempt
def place_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Giriş yapmanız gerekiyor'}, status=401)

    user = User.objects.get(id=user_id)
    cart = Cart.objects.filter(user=user).first()

    if not cart:
        return JsonResponse({'error': 'Sepet boş'}, status=400)

    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        return JsonResponse({'error': 'Sepette ürün yok'}, status=400)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    # 1. Order kaydı oluştur
    order = Order.objects.create(
        user=user,
        total_price=total_price,
        delivery_address=user.delivery_address
    )

    # 2. OrderItem'ları oluştur
    invoice_items = []
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price_at_purchase=item.product.price
        )

        invoice_items.append({
            "name": item.product.name,
            "quantity": item.quantity,
            "price": item.product.price
        })

        # Stoktan düş
        item.product.stock_quantity -= item.quantity
        item.product.save()

    # 3. Fatura PDF'sini oluştur
    pdf_path = generate_invoice_pdf(order.id, user.email, user.delivery_address, invoice_items, total_price)

    # 4. E-posta ile PDF gönder
    send_invoice_email(user.email, pdf_path)

    # 5. Sepeti temizle
    cart_items.delete()

    return JsonResponse({'message': 'Sipariş alındı, fatura gönderildi'})

# Product Manager specific endpoints
@csrf_exempt
@require_http_methods(["PUT"])
def update_order_status(request, order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = User.objects.get(id=user_id)
    if user.role != 1:  # Only product managers can update status
        return JsonResponse({'error': 'Only product managers can update order status'}, status=403)
    
    try:
        data = json.loads(request.body)
        new_status = data.get('status')

        if new_status not in ['processing', 'in-transit', 'delivered']:
            return JsonResponse({'error': 'Invalid status value'}, status=400)

        order = Order.objects.get(id=order_id)
        
        # Validate status transition
        if order.status == 'delivered' and new_status != 'delivered':
            return JsonResponse({'error': 'Cannot change status of delivered order'}, status=400)
        
        if order.status == 'in-transit' and new_status == 'processing':
            return JsonResponse({'error': 'Cannot revert to processing status'}, status=400)

        order.status = new_status
        order.save()

        return JsonResponse({
            'message': f'Order {order_id} updated to {new_status}',
            'order': {
                'id': order.id,
                'status': order.status,
                'delivery_address': order.delivery_address,
                'total_price': float(order.total_price),
                'customer_id': order.user.id,
                'customer_name': order.user.get_full_name() or order.user.username
            }
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def delivery_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = User.objects.get(id=user_id)
    if user.role != 1:  # Only product managers can view delivery list
        return JsonResponse({'error': 'Only product managers can view delivery list'}, status=403)
    
    try:
        # Get all orders with related data
        orders = Order.objects.all().select_related('user').prefetch_related('items__product')

        result = []
        for order in orders:
            items = []
            for item in order.items.all():
                items.append({
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "price_each": float(item.price_at_purchase)
                })

            result.append({
                "delivery_id": order.id,
                "customer_id": order.user.id,
                "customer_name": order.user.get_full_name() or order.user.username,
                "customer_email": order.user.email,
                "total_price": float(order.total_price),
                "delivery_address": order.delivery_address,
                "status": order.status,
                "created_at": order.created_at,
                "items": items
            })

        return JsonResponse({"deliveries": result})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# User specific endpoints
@require_http_methods(["GET"])
def get_latest_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        user = User.objects.get(id=user_id)
        latest_order = Order.objects.filter(user=user).latest('created_at')
        order_items = OrderItem.objects.filter(order=latest_order)
        
        items_data = [
            {
                'product_id': item.product.id,
                'product_name': item.product.name,
                'image_url': item.product.image_url,
                'quantity': item.quantity,
                'price_each': float(item.price_at_purchase)
            }
            for item in order_items
        ]
        
        response_data = {
            'order_id': latest_order.id,
            'created_at': latest_order.created_at,
            'total_price': float(latest_order.total_price),
            'delivery_address': latest_order.delivery_address,
            'status': latest_order.status,
            'items': items_data
        }
        return JsonResponse(response_data)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'No orders found for this user.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_all_orders_for_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        user = User.objects.get(id=user_id)
        orders = Order.objects.filter(user=user).order_by('-created_at')
        
        if not orders.exists():
            return JsonResponse({'message': 'No orders found for this user.'}, status=404)
        
        orders_data = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            items_data = [
                {
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'image_url': item.product.image_url,
                    'quantity': item.quantity,
                    'price_each': float(item.price_at_purchase)
                }
                for item in order_items
            ]
            orders_data.append({
                'order_id': order.id,
                'created_at': order.created_at,
                'total_price': float(order.total_price),
                'delivery_address': order.delivery_address,
                'status': order.status,
                'items': items_data
            })
        return JsonResponse({'orders': orders_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_invoice_details(request, order_id):
    """Get detailed invoice information for a specific order."""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = User.objects.get(id=user_id)
    if user.role != 1:  # Only product managers can view invoice details
        return JsonResponse({'error': 'Only product managers can view invoice details'}, status=403)
    
    try:
        order = Order.objects.select_related('user').prefetch_related('items__product').get(id=order_id)
        
        # Get order items with product details
        items = []
        for item in order.items.all():
            items.append({
                'product_id': item.product.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price_each': float(item.price_at_purchase),
                'total': float(item.price_at_purchase * item.quantity)
            })
        
        # Get invoice PDF path
        invoice_path = f'invoices/invoice_{order.id}.pdf'
        has_invoice = os.path.exists(invoice_path)
        
        response_data = {
            'invoice_id': order.id,
            'customer': {
                'id': order.user.id,
                'name': order.user.get_full_name() or order.user.username,
                'email': order.user.email,
                'address': order.delivery_address
            },
            'order_date': order.created_at,
            'status': order.status,
            'items': items,
            'subtotal': float(order.total_price),
            'has_invoice_pdf': has_invoice,
            'invoice_pdf_url': f'/api/orders/invoice/{order.id}/pdf/' if has_invoice else None
        }
        
        return JsonResponse(response_data)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_invoice_pdf(request, order_id):
    """Get the PDF file of an invoice."""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = User.objects.get(id=user_id)
    if user.role != 1:  # Only product managers can view invoice PDFs
        return JsonResponse({'error': 'Only product managers can view invoice PDFs'}, status=403)
    
    try:
        order = Order.objects.get(id=order_id)
        invoice_path = f'invoices/invoice_{order.id}.pdf'
        
        if not os.path.exists(invoice_path):
            return JsonResponse({'error': 'Invoice PDF not found'}, status=404)
        
        # Generate new PDF if it doesn't exist
        if not os.path.exists(invoice_path):
            items = []
            for item in order.items.all():
                items.append({
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "price": float(item.price_at_purchase)
                })
            generate_invoice_pdf(order.id, order.user.email, order.user.delivery_address, items, float(order.total_price))
        
        # Return the PDF file
        with open(invoice_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename=invoice_{order.id}.pdf'
            return response
            
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def cancel_order(request, order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    try:
        user = User.objects.get(id=user_id)
        order = Order.objects.get(id=order_id)

        # Check if the order belongs to the authenticated user
        if order.user != user:
            return JsonResponse({'error': 'Bu siparişi iptal etme yetkiniz yok.'}, status=403)

        # Check if the order status is 'processing'
        if order.status != 'processing':
            return JsonResponse({'error': 'Sadece işlemde olan siparişler iptal edilebilir.'}, status=400)

        # Update order status to cancelled
        order.status = 'cancelled'
        order.save()

        # Increase product stock quantity
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            product = item.product
            product.stock_quantity += item.quantity
            product.save()

        # Send cancellation email
        items_data = [
            {
                'name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.price_at_purchase),
            }
            for item in order_items
        ]
        send_cancellation_email(user.email, order.id, items_data, float(order.total_price))

        return JsonResponse({'message': f'Sipariş #{order_id} başarıyla iptal edildi.'})

    except Order.DoesNotExist:
        return JsonResponse({'error': 'Sipariş bulunamadı.'}, status=404)
    except User.DoesNotExist:
         return JsonResponse({'error': 'Kullanıcı bulunamadı.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def orders_by_date_range(request):
    """
    Retrieves orders within a specified date range.
    Expects 'start_date' and 'end_date' query parameters in 'YYYY-MM-DD' format.
    """
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        return JsonResponse({'error': "Please provide both 'start_date' and 'end_date' query parameters."},
                        status=400)

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': "Invalid date format. Please use 'YYYY-MM-DD'."},
                        status=400)

    if start_date > end_date:
        return JsonResponse({'error': "'start_date' cannot be after 'end_date'."},
                        status=400)

    orders = Order.objects.filter(created_at__date__range=[start_date, end_date]).select_related('user').prefetch_related('items__product')
    if not orders.exists():
        return JsonResponse({'message': 'No orders found in the specified date range.'}, status=404)

    # Manually serialize the orders
    orders_data = []
    for order in orders:
        items_data = []
        for item in order.items.all():
            items_data.append({
                'product_id': item.product.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price_at_purchase': float(item.price_at_purchase)
            })
        orders_data.append({
            'id': order.id,
            'user_email': order.user.email,
            'created_at': order.created_at.isoformat(),
            'total_price': float(order.total_price),
            'delivery_address': order.delivery_address,
            'status': order.status,
            'items': items_data
        })
    return JsonResponse({'orders': orders_data})

@require_http_methods(["GET"])
def calculate_revenue(request):
    """
    Calculates the total revenue between two specified dates.
    Expects 'start_date' and 'end_date' query parameters in 'YYYY-MM-DD' format.
    """
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        return JsonResponse({'error': "Please provide both 'start_date' and 'end_date' query parameters."},
                        status=400)

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': "Invalid date format. Please use 'YYYY-MM-DD'."},
                        status=400)

    if start_date > end_date:
        return JsonResponse({'error': "'start_date' cannot be after 'end_date'."},
                        status=400)

    # Calculate total revenue for orders in the date range
    orders = Order.objects.filter(created_at__date__range=[start_date, end_date])
    
    # Calculate sum of total_price for all orders in range
    total_revenue = sum(order.total_price for order in orders)
    
    # Count the number of orders
    order_count = orders.count()
    
    # Just return the total revenue amount as requested
    return JsonResponse(float(total_revenue), safe=False)




