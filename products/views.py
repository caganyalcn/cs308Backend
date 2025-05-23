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
from django.core.mail import send_mail
from django.conf import settings

import json
from decimal import Decimal

from .models import Product, Cart, CartItem, Category, Favorite, CreditCard
from .serializers import ProductSerializer, CategorySerializer, FavoriteSerializer
from accounts.models import User
from .models import hash_with_salt

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


@csrf_exempt
@require_http_methods(["POST"])
def update_product_price(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    # Check if the user is a sales manager (role == 2)
    if user.role != 2:
        return JsonResponse({"error": "Only sales managers can update product prices"}, status=403)

    try:
        data = json.loads(request.body)
        new_price = data.get('price')

        if new_price is None:
            return JsonResponse({"error": "Price is required"}, status=400)

        try:
            new_price = float(new_price)
            if new_price < 0:
                return JsonResponse({"error": "Price cannot be negative"}, status=400)
        except ValueError:
            return JsonResponse({"error": "Invalid price format"}, status=400)

        product = Product.objects.get(id=product_id)
        product.price = new_price
        product.save()
        
        # Assuming you have a ProductSerializer
        from .serializers import ProductSerializer 
        return JsonResponse({
            "message": "Product price updated successfully",
            "product": ProductSerializer(product).data
        }, status=200)

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def discount_product(request, product_id):
    # Ensure sales manager
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "Authentication required"}, status=401)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    if user.role != 2:
        return JsonResponse({"error": "Only sales managers can apply discounts"}, status=403)
    # Parse discount
    try:
        data = json.loads(request.body)
        discount_pct = data.get('discount_percentage')
        if discount_pct is None:
            return JsonResponse({"error": "Discount percentage required"}, status=400)
        discount_pct = Decimal(str(discount_pct))
        if discount_pct < 0 or discount_pct > 100:
            return JsonResponse({"error": "Discount percentage must be between 0 and 100"}, status=400)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid discount format"}, status=400)
    # Get product
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    # Check if product price is 0 or null
    if product.price is None or product.price == Decimal('0'):
        return JsonResponse({"error": "Cannot apply discount to a product with no price or zero price."}, status=400)

    # Apply discount using Decimal
    old_price = product.price 
    new_price = old_price * (Decimal('1') - discount_pct / Decimal('100'))
    product.price = new_price
    product.save()
    # Notify users who favorited the product
    favorites = Favorite.objects.filter(product=product).select_related('user')
    recipient_list = [fav.user.email for fav in favorites if fav.user.email]
    if recipient_list:
        subject = f"{product.name} ürününde {discount_pct}% indirim!"
        message = (
            f"Merhaba! '{product.name}' ürününde %{discount_pct} indirim var. "
            f"Yeni fiyatı {new_price:.2f} TL."
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return JsonResponse({
        "message": "Discount applied successfully",
        "product": ProductSerializer(product).data
    }, status=200)

@csrf_exempt
@api_view(['POST'])
def add_to_favorites(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)
    except (json.JSONDecodeError, Product.DoesNotExist):
        return JsonResponse({'error': 'Invalid product'}, status=400)
    user = User.objects.get(id=user_id)
    if Favorite.objects.filter(user=user, product=product).exists():
        return JsonResponse({'message': 'Already in favorites'})
    Favorite.objects.create(user=user, product=product)
    return JsonResponse({'message': 'Added to favorites'})

@csrf_exempt
@api_view(['POST'])
def remove_from_favorites(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        fav = Favorite.objects.filter(user_id=user_id, product_id=product_id).first()
        if fav:
            fav.delete()
            return JsonResponse({'message': 'Removed from favorites'})
    except json.JSONDecodeError:
        pass
    return JsonResponse({'error': 'Favorite not found'}, status=404)

@csrf_exempt
@api_view(['GET'])
def get_favorites(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'favorites': []})
    favs = Favorite.objects.filter(user_id=user_id).select_related('product')
    serializer = FavoriteSerializer(favs, many=True)
    return JsonResponse({'favorites': serializer.data})

@csrf_exempt
@require_http_methods(["POST"])
def save_credit_card_details(request):
    # Check for user authentication via session
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    try:
        # Fetch the user based on the session ID
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    try:
        data = json.loads(request.body)
        card_number = data.get('card_number')
        cvv = data.get('cvv')
        expiry_date = data.get('expiry_date')
        card_holder_name = data.get('card_holder_name')

        if not all([card_number, cvv, expiry_date, card_holder_name]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Hash card number and CVV using the utility function
        card_number_hash_hex, card_number_salt_hex = hash_with_salt(card_number)
        cvv_hash_hex, cvv_salt_hex = hash_with_salt(cvv)

        # Create and save the CreditCard instance
        credit_card = CreditCard.objects.create(
            user=user,
            card_number_hash=card_number_hash_hex,
            card_number_salt=card_number_salt_hex,
            cvv_hash=cvv_hash_hex,
            cvv_salt=cvv_salt_hex,
            expiry_date=expiry_date,
            card_holder_name=card_holder_name,
        )

        return JsonResponse({'message': 'Credit card details saved successfully', 'card_id': credit_card.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

