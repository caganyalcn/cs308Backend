from django.urls import path
from .views import (
    ProductListView, 
    ProductDetailView, 
    update_stock
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/stock/update/', update_stock, name='update-stock'),
]
