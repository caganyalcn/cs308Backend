from rest_framework.decorators import api_view
from .models import Review
from .serializers import ReviewSerializer
from orders.models import OrderItem
from accounts.models import User
from products.models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import models
from django.views.decorators.http import require_http_methods

# Helper function to check if a user is a product manager (assuming role 1 is product manager)
def is_product_manager(user):
    return user.role == 1

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
    """Get all reviews with a rating or a comment for a specific product. Comments are only shown if approved."""
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
    """Get all reviews by the current user (both approved and pending)."""
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return JsonResponse(serializer.data)

@require_http_methods(["GET"])
def list_all_reviews(request):
    """Lists all reviews for product managers (including unapproved)."""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        user = User.objects.get(id=user_id)
        if not is_product_manager(user):
            return JsonResponse({'error': 'Only product managers can view all reviews'}, status=403)
        
        reviews = Review.objects.all().select_related('user', 'product').order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        # Include user name and product name in the response
        data = serializer.data
        for review_data in data:
             review_obj = reviews.get(id=review_data['id'])
             review_data['customer_name'] = review_obj.user.get_full_name() or review_obj.user.email
             review_data['product_name'] = review_obj.product.name
             review_data['product_id'] = review_obj.product.id

        return JsonResponse({"reviews": data})
    except User.DoesNotExist:
         return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_review_approval(request, review_id):
    """Updates the approval status of a review (Product Manager only)."""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        user = User.objects.get(id=user_id)
        if not is_product_manager(user):
            return JsonResponse({'error': 'Only product managers can update review approval'}, status=403)
        
        try:
            data = json.loads(request.body)
            is_approved = data.get('is_approved')
            if is_approved is None:
                 return JsonResponse({'error': 'is_approved field is required'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        try:
            review = Review.objects.get(id=review_id)
            review.approved = bool(is_approved)
            
            # Store original comment before rejection
            original_comment = review.comment
            
            # If rejecting, set comment to rejection message
            if not review.approved:
                review.comment = f"{original_comment}\n\n -- This comment is rejected"
            
            review.save()

            # Re-calculate avg_rating and rating_count for the product
            product = review.product
            all_ratings = Review.objects.filter(product=product, rating__isnull=False, approved=True).values_list('rating', flat=True)
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
                "message": "Review approval status updated successfully", 
                "review": serializer.data,
                "status": "rejected" if not review.approved else "approved"
            })
            
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)
            
    except User.DoesNotExist:
         return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
