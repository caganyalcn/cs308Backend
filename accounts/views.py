from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from .serializers import UserSerializer

<<<<<<< HEAD
=======
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from .serializers import UserSerializer

>>>>>>> 4fc05c4 (Remove .pyc and __pycache__ from version control and update .gitignore)
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            # Print raw request body
            print("Raw request body:", request.body.decode('utf-8'))
            
            data = json.loads(request.body)
            print("Parsed JSON data:", data)
            
            # Validate required fields
            required_fields = ['name', 'surname', 'email', 'password']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return JsonResponse({
                    "message": "Missing required fields",
                    "missing_fields": missing_fields
                }, status=400)
            
            serializer = UserSerializer(data=data)
            print("Serializer is valid:", serializer.is_valid())
            if not serializer.is_valid():
                print("Validation errors:", serializer.errors)
                return JsonResponse({
                    "message": "Validation failed",
                    "errors": serializer.errors,
                    "received_data": data
                }, status=400)
            
            user = serializer.save()
            print("User created successfully:", user.email)
            return JsonResponse({
                "message": "User created successfully",
                "user": UserSerializer(user).data
            })
            
        except json.JSONDecodeError as e:
            print("JSON decode error:", str(e))
            return JsonResponse({
                "message": "Invalid JSON data",
                "error": str(e)
            }, status=400)
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse({
                "message": "An unexpected error occurred",
                "error": str(e)
            }, status=400)
    return JsonResponse({"message": "Signup endpoint works"})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            print("Raw login request body:", request.body.decode('utf-8'))
            data = json.loads(request.body)
            print("Login attempt with data:", data)
            
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return JsonResponse({
                    "message": "Email and password are required"
                }, status=400)
            
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return JsonResponse({
                        "message": "Login successful",
                        "user": UserSerializer(user).data
                    })
                return JsonResponse({"message": "Invalid credentials"}, status=401)
            except User.DoesNotExist:
                return JsonResponse({"message": "User not found"}, status=404)
        except json.JSONDecodeError as e:
            print("Login JSON decode error:", str(e))
            return JsonResponse({
                "message": "Invalid JSON data",
                "error": str(e)
            }, status=400)
        except Exception as e:
            print("Login unexpected error:", str(e))
            return JsonResponse({
                "message": "An unexpected error occurred",
                "error": str(e)
            }, status=400)
    return JsonResponse({"message": "Login endpoint works"})

@csrf_exempt
def get_current_user(request):
    # In a real app, you would get the user from the session or JWT
    # For now, we'll just return a mock response
    return JsonResponse({
        "message": "Current user endpoint works",
        "user": {
            "id": 1,
            "name": "Test User",
            "surname": "Test Surname",
            "email": "test@example.com"
        }
    })


