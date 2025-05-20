"""from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from products.models import Product
from orders.models import Order
from reviews.models import Review
from django.db.models import Q
from datetime import datetime, timedelta
import json
from accounts.authentication import CustomSessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from products.serializers import ProductSerializer



@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    if request.method == 'GET':
        try:
            # Get user from session
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({"message": "Authentication required"}, status=401)
            
            user = User.objects.get(id=user_id)
            if user.role != User.role_product_manager:
                return JsonResponse({"message": "Product-manager access required"}, status=403)
            
            # Get filter parameters from query string
            search_query = request.GET.get('search', '')
            status_filter = request.GET.get('status', '')
            date_filter = request.GET.get('date_range', '')
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            
            # Gather admin dashboard data
            total_users = User.objects.count()
            total_products = Product.objects.count()
            total_orders = Order.objects.count()
            total_reviews = Review.objects.count()
            
            # Base query for orders
            orders_query = Order.objects.all().select_related('user')

            # Apply filters
            if search_query:
                orders_query = orders_query.filter(
                    Q(user__email__icontains=search_query) |
                    Q(user__name__icontains=search_query) |
                    Q(id__icontains=search_query) |
                    Q(items__product__name__icontains=search_query)
                ).distinct()

            if status_filter:
                orders_query = orders_query.filter(status=status_filter)

            if date_filter:
                today = datetime.now()
                if date_filter == 'today':
                    orders_query = orders_query.filter(created_at__date=today.date())
                elif date_filter == 'week':
                    week_ago = today - timedelta(days=7)
                    orders_query = orders_query.filter(created_at__gte=week_ago)
                elif date_filter == 'month':
                    month_ago = today - timedelta(days=30)
                    orders_query = orders_query.filter(created_at__gte=month_ago)

            if min_price:
                orders_query = orders_query.filter(total_price__gte=float(min_price))
            if max_price:
                orders_query = orders_query.filter(total_price__lte=float(max_price))

            # Get recent orders with pagination
            page = int(request.GET.get('page', 1))
            per_page = int(request.GET.get('per_page', 10))
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            
            total_filtered_orders = orders_query.count()
            recent_orders = orders_query.order_by('-created_at')[start_idx:end_idx]
            
            recent_orders_data = [{
                'id': order.id,
                'user_email': order.user.email,
                'user_name': f"{order.user.name} {order.user.surname}",
                'total_price': str(order.total_price),
                'delivery_address': order.delivery_address,
                'status': order.status,
                'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'items': [{
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'price_at_purchase': str(item.price_at_purchase)
                } for item in order.items.all()]
            } for order in recent_orders]
            
            # Get pending reviews
            pending_reviews = Review.objects.filter(approved=False)
            pending_reviews_data = [{
                'id': review.id,
                'product_name': review.product.name,
                'user_email': review.user.email,
                'rating': review.rating,
                'comment': review.comment
            } for review in pending_reviews]
            
            return JsonResponse({
                "message": "Admin dashboard data retrieved successfully",
                "dashboard_data": {
                    "total_users": total_users,
                    "total_products": total_products,
                    "total_orders": total_orders,
                    "total_reviews": total_reviews,
                    "recent_orders": recent_orders_data,
                    "total_filtered_orders": total_filtered_orders,
                    "current_page": page,
                    "total_pages": (total_filtered_orders + per_page - 1) // per_page,
                    "pending_reviews": pending_reviews_data
                }
            })
            
        except Exception as e:
            return JsonResponse({
                "message": "An error occurred",
                "error": str(e)
            }, status=400)
    return JsonResponse({"message": "Method not allowed"}, status=405)

@api_view(['POST'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def approve_review(request, review_id):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({"message": "Authentication required"}, status=401)
            
            user = User.objects.get(id=user_id)
            if user.role != User.role_product_manager:
                return JsonResponse({"message": "Product-manager access required"}, status=403)
            
            review = Review.objects.get(id=review_id)
            review.approved = True
            review.save()
            
            return JsonResponse({
                "message": "Review approved successfully",
                "review_id": review_id
            })
            
        except Review.DoesNotExist:
            return JsonResponse({"message": "Review not found"}, status=404)
        except Exception as e:
            return JsonResponse({
                "message": "An error occurred",
                "error": str(e)
            }, status=400)
    return JsonResponse({"message": "Method not allowed"}, status=405) 

@api_view(['POST'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def add_product(request):
    if request.user.role != User.role_product_manager:
        return Response({"error": "Forbidden"}, status=403)
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product = serializer.save(is_priced=False)
    return Response({"id": product.id, "message": "Product added, waiting for pricing."}, status=201)


@api_view(["PUT"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
 
    try:
        user = request.user
        if user.role != User.role_product_manager:
            return Response({"error": "Unauthorized"}, status=403)
        
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated successfully", "product": serializer.data})
        else:
            return Response(serializer.errors, status=400)
    
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["DELETE"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def remove_product(request, pk):

    try:
        user = request.user
        if user.role != User.role_product_manager:
            return Response({"error": "Unauthorized"}, status=403)

        product = Product.objects.get(pk=pk)
        
        if Order.objects.filter(items__product=product).exists():
            return Response({"error": "This product has existing orders and cannot be deleted."}, status=400)
        
        product.delete()
        return Response({"message": "Product deleted successfully."})
    
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["PUT"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def update_stock(request, pk):

    try:
        user = request.user
        if user.role != User.role_product_manager:
            return Response({"error": "Unauthorized"}, status=403)

        product = Product.objects.get(pk=pk)
        stock_quantity = request.data.get("stock_quantity")

        if stock_quantity is not None and int(stock_quantity) >= 0:
            product.stock_quantity = int(stock_quantity)
            product.save(update_fields=["stock_quantity"])
            return Response({"message": "Stock updated successfully", "quantity": product.stock_quantity})
        else:
            return Response({"error": "Invalid stock quantity."}, status=400)
    
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated])
def disapprove_review(request, review_id):

    try:
        user = request.user
        if user.role != User.role_product_manager:
            return Response({"error": "Unauthorized"}, status=403)

        review = Review.objects.get(pk=review_id)
        review.approved = False
        review.save()
        
        return Response({
            "message": "Review disapproved successfully",
            "review_id": review_id
        })
    
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

"""

# accounts/product_manager_views.py
from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.authentication import CustomSessionAuthentication
from accounts.permission import IsProductManager
from .models import User
from products.models import Product
from orders.models import Order
from reviews.models import Review
from products.serializers import ProductSerializer

@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def admin_dashboard(request):
    # Filtre parametreleri
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date_range', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Dashboard verileri
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_reviews = Review.objects.count()

    # Sipariş sorgusu
    orders_qs = Order.objects.all().select_related('user').prefetch_related('items__product')
    if search:
        orders_qs = orders_qs.filter(
            Q(user__email__icontains=search) |
            Q(user__name__icontains=search) |
            Q(id__icontains=search) |
            Q(items__product__name__icontains=search)
        ).distinct()
    if status_filter:
        orders_qs = orders_qs.filter(status=status_filter)
    if date_filter:
        today = datetime.now()
        if date_filter == 'today':
            orders_qs = orders_qs.filter(created_at__date=today.date())
        elif date_filter == 'week':
            orders_qs = orders_qs.filter(created_at__gte=today - timedelta(days=7))
        elif date_filter == 'month':
            orders_qs = orders_qs.filter(created_at__gte=today - timedelta(days=30))
    if min_price:
        orders_qs = orders_qs.filter(total_price__gte=float(min_price))
    if max_price:
        orders_qs = orders_qs.filter(total_price__lte=float(max_price))

    # Pagination
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    start = (page - 1) * per_page
    end = start + per_page
    total_filtered = orders_qs.count()
    recent = orders_qs.order_by('-created_at')[start:end]

    recent_data = [{
        'id': o.id,
        'user_email': o.user.email,
        'user_name': f"{o.user.name} {o.user.surname}",
        'total_price': str(o.total_price),
        'delivery_address': o.delivery_address,
        'status': o.status,
        'created_at': o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        'items': [{
            'product_name': i.product.name,
            'quantity': i.quantity,
            'price_at_purchase': str(i.price_at_purchase)
        } for i in o.items.all()]
    } for o in recent]

    # Bekleyen yorumlar
    pending = Review.objects.filter(approved=False)
    pending_data = [{
        'id': r.id,
        'product_name': r.product.name,
        'user_email': r.user.email,
        'rating': r.rating,
        'comment': r.comment
    } for r in pending]

    return Response({
        'message': 'Admin dashboard data retrieved successfully',
        'dashboard_data': {
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_reviews': total_reviews,
            'recent_orders': recent_data,
            'total_filtered_orders': total_filtered,
            'current_page': page,
            'total_pages': (total_filtered + per_page - 1) // per_page,
            'pending_reviews': pending_data
        }
    })

@api_view(['POST'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def approve_review(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
        review.approved = True
        review.save()
        return Response({'message': 'Review approved successfully'})
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=404)

@api_view(['POST'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def disapprove_review(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
        review.approved = False
        review.save()
        return Response({'message': 'Review disapproved successfully'})
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=404)

@api_view(['POST'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def add_product(request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product = serializer.save(is_priced=False)
    return Response({'id': product.id, 'message': 'Product added, waiting for pricing.'}, status=201)

@api_view(['PUT'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    serializer = ProductSerializer(product, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'message': 'Product updated successfully', 'product': serializer.data})

@api_view(['DELETE'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def remove_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    if Order.objects.filter(items__product=product).exists():
        return Response({'error': 'Cannot delete, existing orders present'}, status=400)
    product.delete()
    return Response({'message': 'Product deleted successfully'})

@api_view(['PUT'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def update_stock(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    qty = request.data.get('stock_quantity')
    if qty is None or int(qty) < 0:
        return Response({'error': 'Invalid stock quantity'}, status=400)
    product.stock_quantity = int(qty)
    product.save(update_fields=['stock_quantity'])
    return Response({'message': 'Stock updated successfully', 'quantity': product.stock_quantity})