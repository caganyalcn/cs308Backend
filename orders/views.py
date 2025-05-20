"""from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from products.models import Cart, CartItem, Product
from .utils import generate_invoice_pdf
from accounts.models import User
from django.views.decorators.http import require_POST, require_GET
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.core.mail import EmailMessage
from .serializers import OrderSerializer

def send_invoice_email(user_email, pdf_path):
    subject = 'Order Invoice - ÇiftlikBank'
    body = 'Your order has been completed successfully. The invoice is attached.'

    email = EmailMessage(subject, body, to=[user_email])
    email.attach_file(pdf_path)
    email.send()

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

    data = json.loads(request.body or '{}')
    delivery_address = data.get('address', 'Default address')

    # 1. Order kaydı oluştur
    order = Order.objects.create(
        user=user,
        total_price=total_price,
        delivery_address=delivery_address
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
    pdf_path = generate_invoice_pdf(order.id, user.email, invoice_items, total_price)

    # 4. E-posta ile PDF gönder
    send_invoice_email(user.email, pdf_path)

    # 5. Sepeti temizle
    cart_items.delete()

    return JsonResponse({'message': 'Sipariş alındı, fatura gönderildi'})

@csrf_exempt
@require_POST
def update_order_status(request, order_id):
    # session-based authentication
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    user = User.objects.get(id=user_id)
    if not user.is_admin:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    try:
        data = json.loads(request.body)
        new_status = data.get('status')

        if new_status not in ['processing', 'in-transit', 'delivered']:
            return JsonResponse({'error': 'Invalid status value'}, status=400)

        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()

        return JsonResponse({'message': f'Order {order_id} updated to {new_status}'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_GET
def delivery_list(request):
    # session-based authentication
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    user = User.objects.get(id=user_id)
    if not user.is_admin:
        return JsonResponse({'error': 'Permission denied'}, status=403)
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
            "total_price": float(order.total_price),
            "delivery_address": order.delivery_address,
            "status": order.status,
            "items": items
        })

    return JsonResponse({"deliveries": result}, safe=False)

@csrf_exempt
@require_GET
def get_latest_order(request):
    
    #Retrieves the latest order for the currently authenticated user.
    
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    user = User.objects.get(id=user_id)
    
    try:
        latest_order = Order.objects.filter(user=user).latest('created_at')
        # fetch related order items
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

@csrf_exempt
@require_GET
def get_all_orders_for_user(request):
    
    #Retrieves all orders for the currently authenticated user, including their order items.
    
    # Debug logs for session-based auth
    print('get_all_orders_for_user invoked')
    print('Session key:', request.session.session_key)
    user_id = request.session.get('user_id')
    print('Retrieved user_id from session:', user_id)
    if not user_id:
        print('Authentication failed: no user_id in session, returning 401')
        return JsonResponse({'error': 'User not authenticated'}, status=401)
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
    return JsonResponse({'orders': orders_data})"""



# orders/views.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.authentication import CustomSessionAuthentication
from accounts.permissions import IsProductManager
from .models import Order, OrderItem
from products.models import Cart, CartItem
from accounts.models import User
from .utils import generate_invoice_pdf
from django.core.mail import EmailMessage

@api_view(['POST'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    if not cart or not cart.items.exists():
        return Response({'error': 'Cart is empty'}, status=400)
    total = sum(i.product.price * i.quantity for i in cart.items.all())
    address = request.data.get('address', '')
    order = Order.objects.create(user=user, total_price=total, delivery_address=address)
    invoice_items = []
    for item in cart.items.all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price_at_purchase=item.product.price)
        invoice_items.append({'name': item.product.name, 'quantity': item.quantity, 'price': item.product.price})
        item.product.stock_quantity -= item.quantity
        item.product.save()
    pdf_path = generate_invoice_pdf(order.id, user.email, invoice_items, total)
    email = EmailMessage('Order Invoice', 'Your invoice is attached.', to=[user.email])
    email.attach_file(pdf_path)
    email.send()
    cart.items.all().delete()
    return Response({'message': 'Order placed and invoice sent'})

@api_view(['PUT'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    new_status = request.data.get('status')
    if new_status not in ['processing', 'in-transit', 'delivered']:
        return Response({'error': 'Invalid status'}, status=400)
    order.status = new_status
    order.save()
    return Response({'message': f'Order {order_id} updated to {new_status}'})

@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def delivery_list(request):
    orders = Order.objects.all().select_related('user').prefetch_related('items__product')
    data = []
    for o in orders:
        items = [{'product_id': i.product.id, 'product_name': i.product.name, 'quantity': i.quantity, 'price_each': float(i.price_at_purchase)} for i in o.items.all()]
        data.append({'delivery_id': o.id, 'customer_id': o.user.id, 'customer_name': o.user.get_full_name(), 'total_price': float(o.total_price), 'delivery_address': o.delivery_address, 'status': o.status, 'items': items})
    return Response({'deliveries': data})

@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def get_latest_order(request):
    user = request.user
    try:
        latest_order = Order.objects.filter(user=user).latest('created_at')
        items = OrderItem.objects.filter(order=latest_order)
        items_data = [{
            'product_id': i.product.id,
            'product_name': i.product.name,
            'image_url': i.product.image_url,
            'quantity': i.quantity,
            'price_each': float(i.price_at_purchase)
        } for i in items]
        return Response({
            'order_id': latest_order.id,
            'created_at': latest_order.created_at,
            'total_price': float(latest_order.total_price),
            'delivery_address': latest_order.delivery_address,
            'status': latest_order.status,
            'items': items_data
        })
    except Order.DoesNotExist:
        return Response({'message': 'No orders found for this user.'}, status=404)

@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def get_all_orders_for_user(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    if not orders.exists():
        return Response({'message': 'No orders found for this user.'}, status=404)
    orders_data = []
    for o in orders:
        items = OrderItem.objects.filter(order=o)
        items_data = [{
            'product_id': i.product.id,
            'product_name': i.product.name,
            'image_url': i.product.image_url,
            'quantity': i.quantity,
            'price_each': float(i.price_at_purchase)
        } for i in items]
        orders_data.append({
            'order_id': o.id,
            'created_at': o.created_at,
            'total_price': float(o.total_price),
            'delivery_address': o.delivery_address,
            'status': o.status,
            'items': items_data
        })
    return Response({'orders': orders_data})


