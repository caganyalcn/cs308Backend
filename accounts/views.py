from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializer
from products.models import Cart, CartItem
import json

#cart merge func
def merge_carts(request, user):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    # Get guest cart (session-based, no user linked)
    guest_cart = Cart.objects.filter(session_id=session_id, user__isnull=True).first()
    user_cart, _ = Cart.objects.get_or_create(user=user)

    if guest_cart:
        for item in guest_cart.items.all():
            existing = user_cart.items.filter(product=item.product).first()
            if existing:
                existing.quantity += item.quantity
                existing.save()
            else:
                item.cart = user_cart
                item.save()
        guest_cart.delete()


# signup
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# ----------- LOGIN VIEW WITH CART MERGE -----------
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()
        
        if user and user.check_password(password):
            request.session['user_id'] = user.id
            request.session.modified = True

            # Merge cart after login
            merge_carts(request, user)

            return JsonResponse({'message': 'Login successful'})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)




