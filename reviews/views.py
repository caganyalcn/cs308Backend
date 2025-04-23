from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from orders.models import OrderItem

@api_view(['POST'])
@permission_classes([IsAuthenticated])
<<<<<<< HEAD
def add_review(request):
=======
def submit_review(request):
>>>>>>> c5c2500aa43b293b010839f7f5c7a9f7bd1a7009
    user = request.user
    product_id = request.data.get('product')
    rating = request.data.get('rating')
    comment = request.data.get('comment', '')

    from products.models import Product  # imported here to avoid circular import issues

    try:
        product = Product.objects.get(id=product_id)
        purchased = OrderItem.objects.filter(product=product, order__user=user, order__status='delivered').exists()
        if not purchased:
            return Response({'error': 'You can only review delivered products you have purchased.'}, status=403)

        review = Review.objects.create(
            product=product,
            user=user,
            rating=rating,
            comment=comment
        )
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=201)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
