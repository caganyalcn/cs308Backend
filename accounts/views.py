from django.shortcuts import render
from django.http import JsonResponse

def signup(request):
    return JsonResponse({"message": "Signup page works"})

def login(request):
    return JsonResponse({"message": "Login page works"})

