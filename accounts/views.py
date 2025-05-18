from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from .serializers import UserSerializer
from products.models import Cart, CartItem
from django.contrib.auth.hashers import make_password
from django.conf import settings

# Utility function to merge guest cart into user cart
def merge_guest_cart_to_user(request, user):
    session_id = request.session.session_key
    if not session_id:
        return
    guest_cart = Cart.objects.filter(session_id=session_id, user__isnull=True).first()
    if not guest_cart:
        return
    user_cart = Cart.objects.filter(user=user).first()
    if user_cart:
        # Merge guest cart items into user cart
        for guest_item in guest_cart.items.all():
            try:
                user_item = user_cart.items.get(product=guest_item.product)
                user_item.quantity += guest_item.quantity
                user_item.save()
            except CartItem.DoesNotExist:
                guest_item.cart = user_cart
                guest_item.save()
        guest_cart.delete()
    else:
        # No cart for user, assign guest cart to user
        guest_cart.user = user
        guest_cart.session_id = None
        guest_cart.save()

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"message": "Login endpoint works"})

    try:
        data = json.loads(request.body)
        email = data.get("email")
        raw_password = data.get("password")

        if not email or not raw_password:
            return JsonResponse({"message": "Email and password are required"}, status=400)

        # 1️⃣ Satış yöneticisi
        if email == settings.SALES_MANAGER_EMAIL and raw_password == settings.SALES_MANAGER_PASSWORD:
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={
                    "name": "Sales",
                    "surname": "Manager",
                    "password": make_password(raw_password),
                    "role": "sales_manager",
                },
            )
            if user.role != "sales_manager":
                user.role = "sales_manager"
                user.save(update_fields=["role"])

            # ⬇ Session oluştur
            request.session["user_id"] = user.id
            request.session.save()

            return JsonResponse({"message": "Login successful", "role": user.role})

        # 2️⃣ Normal kullanıcılar
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)

        if not user.check_password(raw_password):
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        request.session["user_id"] = user.id
        request.session.save()
        merge_guest_cart_to_user(request, user)

        return JsonResponse({
            "message": "Login successful",
            "user": UserSerializer(user).data,
            "role": user.role,
        })

    except json.JSONDecodeError as e:
        return JsonResponse({"message": "Invalid JSON data", "error": str(e)}, status=400)
    except Exception as e:
        print("Login unexpected error:", e)
        return JsonResponse({"message": "An unexpected error occurred", "error": str(e)}, status=400)



@csrf_exempt
def get_current_user(request):
   
    if not request.session.session_key:
        request.session.save()
        print("Session initialized with key:", request.session.session_key)
    
    user_id = request.session.get('user_id')
   
    
    if not user_id:
        return JsonResponse({
            "message": "Not authenticated",
            "user": None,
            "session_exists": bool(request.session.session_key)
        }, status=401)
    
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            "message": "Current user retrieved successfully",
            "user": UserSerializer(user).data
        })
    except User.DoesNotExist:
        # Clear invalid session
        request.session.flush()
        return JsonResponse({
            "message": "User not found",
            "user": None
        }, status=404)

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        try:
            # Get the current user's cart before clearing session
            user_id = request.session.get('user_id')
            if user_id:
                # If user is authenticated, ensure their cart is saved
                cart = Cart.objects.filter(user_id=user_id).first()
                if cart:
                    # Cart is already associated with user, no need to transfer
                    pass
            else:
                # If guest, preserve their cart by clearing the session_id
                session_id = request.session.session_key
                if session_id:
                    guest_cart = Cart.objects.filter(session_id=session_id).first()
                    if guest_cart:
                        # Keep the cart but clear the session_id
                        guest_cart.session_id = None
                        guest_cart.save()

            # Clear the session
            request.session.flush()
            
            return JsonResponse({
                "message": "Logged out successfully"
            })
        except Exception as e:
            return JsonResponse({
                "message": "An error occurred during logout",
                "error": str(e)
            }, status=500)
    return JsonResponse({"message": "Method not allowed"}, status=405)


