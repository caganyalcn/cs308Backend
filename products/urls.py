from django.urls import path

from .views import (
    ProductListView, 
    ProductDetailView, 
    add_to_cart,
    get_cart,
    remove_from_cart,
    update_cart_quantity, 
)


urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', add_to_cart, name='add-to-cart'),  
    path('get-cart/', get_cart, name='get-cart'), 
    path('remove-from-cart/', remove_from_cart, name='remove-from-cart'),
    path('update-cart/', update_cart_quantity, name='update-cart'),
]
