from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from orders.models import OrderItem

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    user = request.user
    product_id = request.data.get('product')
    rating = request.data.get('rating')
    comment = request.data.get('comment', '').strip()

    from products.models import Product  # imported here to avoid circular import issues

    try:
        product = Product.objects.get(id=product_id)
        
        # Check if user has ordered the product
        has_order = OrderItem.objects.filter(
            product=product, 
            order__user=user
        ).exists()
        
        if not has_order:
            return Response(
                {'error': 'You can only review products you have ordered.'}, 
                status=403
            )

        # If there's a comment, check if the order is delivered
        if comment:
            is_delivered = OrderItem.objects.filter(
                product=product, 
                order__user=user,
                order__status='delivered'
            ).exists()
            
            if not is_delivered:
                return Response(
                    {'error': 'You can only add comments to delivered products.'}, 
                    status=403
                )

        # Check if user already reviewed this product
        existing_review = Review.objects.filter(product=product, user=user).first()
        if existing_review:
            return Response(
                {'error': 'You have already reviewed this product.'}, 
                status=400
            )

        review = Review.objects.create(
            product=product,
            user=user,
            rating=rating,
            comment=comment,
            approved=False if comment else True  # Auto-approve if only rating
        )
        serializer = ReviewSerializer(review)
        
        response_message = 'Rating submitted successfully.'
        if comment:
            response_message = 'Review submitted successfully. Your comment will be visible after admin approval.'
            
        return Response({
            'message': response_message,
            'review': serializer.data
        }, status=201)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

@api_view(['GET'])
def get_product_reviews(request, product_id):
    """Get all approved reviews for a specific product."""
    try:
        reviews = Review.objects.filter(
            product_id=product_id,
            approved=True
        ).order_by('-created_at')
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_reviews(request):
    """Get all reviews by the current user (both approved and pending)."""
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
