from django.conf import settings
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login as auth_login, logout as auth_logout

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.authentication import CustomSessionAuthentication
from .models import User
from .serializers import UserSerializer
from products.models import Cart, CartItem


def merge_guest_cart_to_user(request, user):

    session_id = request.session.session_key
    if not session_id:
        return
    guest_cart = Cart.objects.filter(session_id=session_id, user__isnull=True).first()
    if not guest_cart:
        return
    user_cart = Cart.objects.filter(user=user).first()
    if user_cart:
        for guest_item in guest_cart.items.all():
            try:
                existing = user_cart.items.get(product=guest_item.product)
                existing.quantity += guest_item.quantity
                existing.save()
            except CartItem.DoesNotExist:
                guest_item.cart = user_cart
                guest_item.save()
        guest_cart.delete()
    else:
        guest_cart.user = user
        guest_cart.session_id = None
        guest_cart.save()


@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token(request):

    token = get_token(request)
    return Response({'csrfToken': token})


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    data = request.data
    email = data.get('email')
    raw_password = data.get('password')
    if not email or not raw_password:
        return Response({'message': 'Email and password are required'}, status=400)

    # ——— 1️⃣ Sales Manager girişi ———
    if email == settings.SALES_MANAGER_EMAIL and raw_password == settings.SALES_MANAGER_PASSWORD:
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                'name': 'Sales',
                'surname': 'Manager',
                'password': make_password(raw_password),
                'role': 'sales_manager',
            }
        )
        if user.role != 'sales_manager':
            user.role = 'sales_manager'
            user.save(update_fields=['role'])

        auth_login(request, user)
        return Response({'message': 'Login successful', 'role': user.role})

    # ——— 2️⃣ Normal kullanıcı girişi ———
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)

    if not user.check_password(raw_password):
        return Response({'message': 'Invalid credentials'}, status=401)

    auth_login(request, user)
    merge_guest_cart_to_user(request, user)
    return Response({
        'message': 'Login successful',
        'user': UserSerializer(user).data,
        'role': user.role
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomSessionAuthentication])
def get_current_user(request):

    user = request.user
    return Response({
        'message': 'Current user retrieved successfully',
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomSessionAuthentication])
def logout(request):

    # (isteğe bağlı) misafir sepetini koruma
    user = request.user
    if not user.is_anonymous:
        # zaten cart.user=user bağlıysa hiçbir şey yapmaya gerek yok
        pass
    else:
        # guest cart için session_id'yi temizle
        session_id = request.session.session_key
        if session_id:
            guest_cart = Cart.objects.filter(session_id=session_id).first()
            if guest_cart:
                guest_cart.session_id = None
                guest_cart.save()

    auth_logout(request)
    return Response({'message': 'Logged out successfully'})




