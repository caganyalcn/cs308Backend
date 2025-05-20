"""from .models import Review
from .serializers import ReviewSerializer
from orders.models import OrderItem
from accounts.models import User
from products.models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import models
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from accounts.permissions import IsProductManager

@csrf_exempt
@api_view(['POST'])
def add_review(request):
    # Debug session info
    print('Headers:', request.headers)
    print('Cookies:', request.COOKIES)
    print('Session key:', request.session.session_key)
    print('Session data:', dict(request.session))
    
    # Get user from session
    user_id = request.session.get('user_id')
    if not user_id:
        print("No user_id in session")
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        user = User.objects.get(id=user_id)
        print(f"Found user: {user.email}")
        
        # Get product and rating from request
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            rating = data.get('rating')
            comment = data.get('comment', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)
        
        # Require at least one of rating or comment
        if (rating is None or rating == "") and (not comment):
            return JsonResponse({'error': 'You must provide either a rating or a comment.'}, status=400)
            
        try:
            product = Product.objects.get(id=product_id)
            print(f"Found product: {product.name}")
            
            # Check if user has ordered the product and it's delivered
            has_delivered_order = OrderItem.objects.filter(
                product=product, 
                order__user=user,
                order__status='delivered'
            ).exists()
            
            if not has_delivered_order:
                print("No delivered order found for this product")
                return JsonResponse(
                    {'error': 'You can only review products you have ordered and received.'}, 
                    status=403
                )
            
            # Check if user already reviewed this product
            existing_review = Review.objects.filter(product=product, user=user).first()
            if existing_review:
                # Update logic (as you have)
                review = existing_review
                updated = False
                if rating is not None and rating != "":
                    review.rating = rating
                    updated = True
                if comment:
                    review.comment = comment
                    review.approved = False  # Needs re-approval
                    updated = True
                if updated:
                    review.save()
                response_message = 'Review updated successfully.'
                if comment and (rating is None or rating == ""):
                    response_message = 'Comment updated successfully. Your comment will be visible after admin approval.'
                elif rating is not None and rating != "" and not comment:
                    response_message = 'Rating updated successfully.'
                elif rating is not None and rating != "" and comment:
                    response_message = 'Review updated successfully. Your comment will be visible after admin approval.'
            else:
                # Create new review
                review = Review.objects.create(
                    product=product,
                    user=user,
                    rating=rating if rating is not None and rating != "" else None,
                    comment=comment,
                    approved=False if comment else True  # Only auto-approve if no comment
                )
                response_message = 'Review submitted successfully.'
                if comment and (rating is None or rating == ""):
                    response_message = 'Comment submitted successfully. Your comment will be visible after admin approval.'
                elif rating is not None and rating != "" and not comment:
                    response_message = 'Rating submitted successfully.'
                elif rating is not None and rating != "" and comment:
                    response_message = 'Review submitted successfully. Your comment will be visible after admin approval.'

            # Update product avg_rating and rating_count if rating is present
            if rating is not None and rating != "":
                all_ratings = Review.objects.filter(product=product, rating__isnull=False).values_list('rating', flat=True)
                ratings_list = list(map(int, all_ratings))
                if ratings_list:
                    product.rating_count = len(ratings_list)
                    product.avg_rating = sum(ratings_list) / product.rating_count
                else:
                    product.rating_count = 0
                    product.avg_rating = 0
                product.save()

            serializer = ReviewSerializer(review)
            return JsonResponse({
                'message': response_message,
                'review': serializer.data
            }, status=201 if not existing_review else 200)
            
        except Product.DoesNotExist:
            print(f"Product not found: {product_id}")
            return JsonResponse({'error': 'Product not found'}, status=404)
            
    except User.DoesNotExist:
        print(f"User not found: {user_id}")
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
def get_product_reviews(request, product_id):
    #Get all reviews with a rating or a comment for a specific product. Comments are only shown if approved.
    try:
        reviews = Review.objects.filter(
            product_id=product_id
        ).filter(
            models.Q(rating__isnull=False) | ~models.Q(comment="")
        ).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        # Hide unapproved comments
        data = serializer.data
        for review in data:
            if not review['approved']:
                review['comment'] = ''
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@api_view(['GET'])
def get_my_reviews(request):
    #Get all reviews by the current user (both approved and pending).
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return JsonResponse(serializer.data)

@api_view(['GET'])
@permission_classes([IsProductManager])
def pending_reviews(request):
    qs = Review.objects.filter(comment__gt='', approved=False).order_by('created_at')
    serializer = ReviewSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsProductManager])
def approve_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.is_approved = True
    comment.save()
    return Response({'message': 'Comment approved'})"""


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from accounts.permissions import IsProductManager
from .models import Review
from .serializers import ReviewSerializer
from orders.models import OrderItem
from products.models import Product

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    user = request.user
    product_id = request.data.get('product_id')
    rating = request.data.get('rating')
    comment = request.data.get('comment', '').strip()
    if not product_id or (rating in [None, ''] and not comment):
        return Response({'error': 'Rating or comment required'}, status=400)
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    if not OrderItem.objects.filter(order__user=user, product=product, order__status='delivered').exists():
        return Response({'error': 'Cannot review without purchase'}, status=403)
    review, created = Review.objects.get_or_create(user=user, product=product, defaults={'rating': rating, 'comment': comment, 'approved': False if comment else True})
    if not created:
        review.rating = rating if rating not in [None, ''] else review.rating
        if comment:
            review.comment = comment
            review.approved = False
        review.save()
    # update product aggregate
    ratings = list(Review.objects.filter(product=product, rating__isnull=False).values_list('rating', flat=True))
    product.rating_count = len(ratings)
    product.avg_rating = sum(ratings) / product.rating_count if ratings else 0
    product.save()
    return Response({'review': ReviewSerializer(review).data})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_reviews(request, product_id):
    qs = Review.objects.filter(product_id=product_id).order_by('-created_at')
    data = ReviewSerializer(qs, many=True).data
    for r in data:
        if not r['approved']:
            r['comment'] = ''
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_reviews(request):
    qs = Review.objects.filter(user=request.user).order_by('-created_at')
    return Response(ReviewSerializer(qs, many=True).data)

@api_view(['GET'])
@permission_classes([IsProductManager])
def pending_reviews(request):
    qs = Review.objects.filter(approved=False, comment__gt='').order_by('created_at')
    return Response(ReviewSerializer(qs, many=True).data)

@api_view(['POST'])
@permission_classes([IsProductManager])
def approve_comment(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=404)
    review.approved = True
    review.save()
    return Response({'message': 'Comment approved'})