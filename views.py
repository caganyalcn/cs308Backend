from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# List all products (with search & filtering)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
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
