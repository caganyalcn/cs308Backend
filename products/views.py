from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError


# List all products (with search & filtering)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
    
        # Filter by category (optional)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__icontains=category)

        # Filter by search (in name OR description)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) | models.Q(description__icontains=search)
            )

        # Sort handling
        sort = self.request.query_params.get('sort', None)
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'popularity':  # Requires a field like num_orders or rating
            queryset = queryset.order_by('rating')  # TEMP placeholder
    
        return queryset
    

# Get a single product
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cart, CartItem, Product
from django.contrib.sessions.models import Session

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        product = Product.objects.filter(id=product_id).first()
        if not product or product.stock_quantity < quantity:
            return JsonResponse({'error': 'Product out of stock'}, status=400)

        # Check if user is logged in
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key

            cart, created = Cart.objects.get_or_create(session_id=session_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        return JsonResponse({'message': 'Added to cart', 'cart_id': cart.id})


def get_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        if not session_id:
            return JsonResponse({'cart': []})
        cart = Cart.objects.filter(session_id=session_id).first()

    if not cart:
        return JsonResponse({'cart': []})

    cart_items = cart.items.all()
    cart_data = [{"product": item.product.name, "quantity": item.quantity, "price": item.total_price()} for item in cart_items]

    return JsonResponse({'cart': cart_data})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_stock(request):
    """
    Update stock for one or multiple products.
    Can handle both single product updates and bulk updates.
    
    Expected request format for single product:
    {
        "product_id": 1,
        "quantity_change": 10,
        "operation": "add"  // or "subtract"
    }
    
    Expected request format for multiple products:
    {
        "updates": [
            {
                "product_id": 1,
                "quantity_change": 10,
                "operation": "add"
            },
            {
                "product_id": 2,
                "quantity_change": 5,
                "operation": "subtract"
            }
        ]
    }
    """
    # Check if this is a bulk update
    updates = request.data.get('updates', [])
    
    # If no updates list, treat as single product update
    if not updates:
        product_id = request.data.get('product_id')
        quantity_change = request.data.get('quantity_change')
        operation = request.data.get('operation', 'add')
        
        if not all([product_id, quantity_change]):
            return Response(
                {'error': 'Missing required fields for single product update'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert single update to list format for consistent processing
        updates = [{
            'product_id': product_id,
            'quantity_change': quantity_change,
            'operation': operation
        }]
    
    results = []
    for update in updates:
        product_id = update.get('product_id')
        quantity_change = update.get('quantity_change')
        operation = update.get('operation', 'add')
        
        if not all([product_id, quantity_change]):
            results.append({
                'product_id': product_id,
                'success': False,
                'error': 'Missing required fields'
            })
            continue
            
        try:
            product = Product.objects.get(id=product_id)
            
            if operation == 'add':
                product.stock_quantity += quantity_change
            elif operation == 'subtract':
                if product.stock_quantity < quantity_change:
                    raise ValidationError('Insufficient stock')
                product.stock_quantity -= quantity_change
            else:
                raise ValidationError('Invalid operation. Use "add" or "subtract"')
                
            product.save()
            
            results.append({
                'product_id': product_id,
                'success': True,
                'current_stock': product.stock_quantity,
                'name': product.name
            })
            
        except Product.DoesNotExist:
            results.append({
                'product_id': product_id,
                'success': False,
                'error': 'Product not found'
            })
        except ValidationError as e:
            results.append({
                'product_id': product_id,
                'success': False,
                'error': str(e)
            })
        except Exception as e:
            results.append({
                'product_id': product_id,
                'success': False,
                'error': str(e)
            })
    
    # If it was a single product update, return a simpler response
    if len(updates) == 1 and 'updates' not in request.data:
        result = results[0]
        if result['success']:
            return Response({
                'message': 'Stock updated successfully',
                'current_stock': result['current_stock'],
                'product_name': result['name']
            })
        else:
            return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
    
    # For bulk updates, return all results
    return Response({'results': results})
