from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

import json

from .models import Product, Cart, CartItem, Category
from .serializers import ProductSerializer, CategorySerializer
from accounts.models import User

# ✅ Ürünleri listeleme (filtreleme, arama, sıralama)
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        category = self.request.query_params.get('category')
        if category:
            try:
                category_id = int(category)
                queryset = queryset.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        sort = self.request.query_params.get('sort')

        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'popularity':
            queryset = queryset.order_by('-rating')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"products": serializer.data})

# ✅ Tek ürün detay görüntüleme

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ✅ Sepete ürün ekleme (frontend çağırır)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 1))

        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)

        # Get product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Ürün bulunamadı'}, status=404)

        # Check stock
        if product.stock_quantity < quantity:
            return JsonResponse({'error': 'Yetersiz stok'}, status=400)

        # Get or create cart
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.filter(user=user).first()
            if not cart:
                cart = Cart.objects.create(user=user)
        else:
            if not request.session.session_key:
                request.session.create()
                request.session.save()
            session_id = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_id=session_id)

        # Get or create cart item
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )

        return JsonResponse({
            'message': 'Sepete eklendi',
            'cart_id': cart.id,
            'item_id': cart_item.id
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ✅ Sepeti detaylı göster (ürün ID, image_url vs. dahil)
@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])

def get_cart(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        cart = Cart.objects.filter(user=user).first()
    else:
        session_id = request.session.session_key
        if not session_id:
            return JsonResponse({'cart': []})
        cart = Cart.objects.filter(session_id=session_id).first()

    if not cart:
        return JsonResponse({'cart': []})


    cart_items = cart.items.select_related('product').all()

    cart_data = [{
        "id": item.product.id,
        "name": item.product.name,
        "image_url": item.product.image_url,
        "description": item.product.description,
        "price": str(item.product.price),
        "quantity": item.quantity,
        "stock_quantity": item.product.stock_quantity,
    } for item in cart_items]

    return JsonResponse({'cart': cart_data})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")

        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.filter(user=user).first()
        else:
            session_id = request.session.session_key
            if not session_id:
                return JsonResponse({'error': 'Session not found'}, status=400)
            cart = Cart.objects.filter(session_id=session_id).first()

        if not cart:
            return JsonResponse({'error': 'Cart not found'}, status=404)

        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if item:
            item.delete()

        return JsonResponse({'message': 'Ürün sepetten çıkarıldı'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def update_cart_quantity(request):
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        new_quantity = int(data.get("quantity"))

        if new_quantity < 1:
            return JsonResponse({'error': 'Adet 1\'den küçük olamaz'}, status=400)

        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.filter(user=user).first()
        else:
            session_id = request.session.session_key
            if not session_id:
                return JsonResponse({'error': 'Session not found'}, status=400)
            cart = Cart.objects.filter(session_id=session_id).first()

        if not cart:
            return JsonResponse({'error': 'Cart not found'}, status=404)

        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if not item:
            return JsonResponse({'error': 'Item not in cart'}, status=404)

        item.quantity = new_quantity
        item.save()

        return JsonResponse({'message': 'Adet güncellendi'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def is_product_manager(user):
    return user.role == 1

@csrf_exempt
@require_http_methods(["POST"])
def create_product(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can create products"}, status=403)
    
    try:
        data = json.loads(request.body)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            return JsonResponse({
                "message": "Product created successfully",
                "product": ProductSerializer(product).data
            }, status=201)
        return JsonResponse({"error": serializer.errors}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_product(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can update products"}, status=403)
    
    try:
        product = Product.objects.get(id=product_id)
        data = json.loads(request.body)
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            return JsonResponse({
                "message": "Product updated successfully",
                "product": ProductSerializer(product).data
            })
        return JsonResponse({"error": serializer.errors}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can delete products"}, status=403)
    
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({"message": "Product deleted successfully"})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@require_http_methods(["GET"])
def list_products(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({"products": serializer.data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# Category Management Views
@csrf_exempt
@require_http_methods(["POST"])
def create_category(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can create categories"}, status=403)
    
    try:
        data = json.loads(request.body)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            category = serializer.save()
            return JsonResponse({
                "message": "Category created successfully",
                "category": CategorySerializer(category).data
            }, status=201)
        return JsonResponse({"error": serializer.errors}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_category(request, category_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can update categories"}, status=403)
    
    try:
        category = Category.objects.get(id=category_id)
        data = json.loads(request.body)
        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            category = serializer.save()
            return JsonResponse({
                "message": "Category updated successfully",
                "category": CategorySerializer(category).data
            })
        return JsonResponse({"error": serializer.errors}, status=400)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_category(request, category_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can delete categories"}, status=403)
    
    try:
        category = Category.objects.get(id=category_id)
        # Check if category has any products
        if Product.objects.filter(category=category).exists():
            return JsonResponse({
                "error": "Cannot delete category with associated products"
            }, status=400)
        category.delete()
        return JsonResponse({"message": "Category deleted successfully"})
    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@require_http_methods(["GET"])
def list_categories(request):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        response_data = {"categories": serializer.data}
        print("Sending categories response:", response_data)  # Debug log
        return JsonResponse(response_data)
    except Exception as e:
        print("Error in list_categories:", str(e))  # Debug log
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_stock(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can update stock"}, status=403)
    
    try:
        product = Product.objects.get(id=product_id)
        data = json.loads(request.body)
        new_quantity = int(data.get('stock_quantity', 0))

        if new_quantity < 0:
            return JsonResponse({"error": "Stock cannot be negative"}, status=400)

        product.stock_quantity = new_quantity
        product.save()

        return JsonResponse({
            "message": "Stock updated successfully",
            "product": ProductSerializer(product).data
        })
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@require_http_methods(["GET"])
def get_stock_history(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can view stock history"}, status=403)
    
    try:
        product = Product.objects.get(id=product_id)
        history = StockHistory.objects.filter(product=product).order_by('-created_at')
        serializer = StockHistorySerializer(history, many=True)
        return JsonResponse({"stock_history": serializer.data})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@require_http_methods(["GET"])
def get_low_stock_products(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can view low stock products"}, status=403)
    
    try:
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=models.F('low_stock_threshold')
        )
        serializer = ProductSerializer(low_stock_products, many=True)
        return JsonResponse({"low_stock_products": serializer.data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_low_stock_threshold(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    user = User.objects.get(id=user_id)
    if not is_product_manager(user):
        return JsonResponse({"error": "Only product managers can update low stock threshold"}, status=403)
    
    try:
        product = Product.objects.get(id=product_id)
        data = json.loads(request.body)
        new_threshold = int(data.get('low_stock_threshold', 10))

        if new_threshold < 0:
            return JsonResponse({"error": "Threshold cannot be negative"}, status=400)

        product.low_stock_threshold = new_threshold
        product.save()

        return JsonResponse({
            "message": "Low stock threshold updated successfully",
            "product": ProductSerializer(product).data
        })
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

