from rest_framework.decorators import api_view
from .models import Review
from .serializers import ReviewSerializer
from orders.models import OrderItem
from accounts.models import User
from products.models import Product
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def add_review(request):
    userid = request.session.get('user_id')
    
    if not userid:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        user = User.objects.get(id=userid)
        
        product_id = request.data.get('product')
        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)
        rating = request.data.get('rating')
        if not rating:
            return JsonResponse({'error': 'Rating is required'}, status=400)
        comment = request.data.get('comment', '').strip()
        

        try:
            product = Product.objects.get(id=product_id)
            
            # Check if user has ordered the product
            has_order = OrderItem.objects.filter(
                product=product, 
                order__user=user,
                order__status='delivered'
            ).exists()
            
            if not has_order:
                return JsonResponse(
                    {'error': 'You can only review products you have ordered.'}, 
                    status=403
                )

            
            # Check if user already reviewed this product
            existing_review = Review.objects.filter(product=product, user=user).first()
            if existing_review:
                return JsonResponse(
                    {'error': 'You have already reviewed this product.'}, 
                    status=400
                )

            review = Review.objects.create(
                product=product,
                user=user,
                rating=rating,
                comment=comment,
                approved=False
            )
            serializer = ReviewSerializer(review)
            
            response_message = 'Rating submitted successfully.'
            if comment:
                response_message = 'Review submitted successfully. Your comment will be visible after admin approval.'
                
            return JsonResponse({
                'message': response_message,
                'review': serializer.data
            }, status=201)

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
            
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
@api_view(['GET'])
def get_product_reviews(request, product_id):
    """Get all approved reviews for a specific product."""
    try:
        reviews = Review.objects.filter(
            product_id=product_id,
            approved=True
        ).order_by('-created_at')
        
        serializer = ReviewSerializer(reviews, many=True)
        return JsonResponse(serializer.data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@api_view(['GET'])
def get_my_reviews(request):
    """Get all reviews by the current user (both approved and pending)."""
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return JsonResponse(serializer.data)
