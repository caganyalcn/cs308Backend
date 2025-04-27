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

import json

from .models import Product, Cart, CartItem
from .serializers import ProductSerializer
from accounts.models import User

# ✅ Ürünleri listeleme (filtreleme, arama, sıralama)
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)

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

