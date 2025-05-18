from django.urls import path
from .views import hello_sales

urlpatterns = [
    path("hello/", hello_sales),
]
