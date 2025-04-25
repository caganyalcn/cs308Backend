from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from products.models import Product
from orders.models import Order
from reviews.models import Review
from django.db.models import Q
from datetime import datetime, timedelta
import json

@csrf_exempt
def admin_dashboard(request):
    if request.method == 'GET':
        try:
            # Get user from session
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({"message": "Authentication required"}, status=401)
            
            user = User.objects.get(id=user_id)
            if not user.is_admin:
                return JsonResponse({"message": "Admin access required"}, status=403)
            
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

@csrf_exempt
def approve_review(request, review_id):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({"message": "Authentication required"}, status=401)
            
            user = User.objects.get(id=user_id)
            if not user.is_admin:
                return JsonResponse({"message": "Admin access required"}, status=403)
            
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