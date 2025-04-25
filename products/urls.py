from django.urls import path
<<<<<<< HEAD
from .views import (
    ProductListView, 
    ProductDetailView, 
    update_stock
)
=======

from .views import (
    ProductListView, 
    ProductDetailView, 
    add_to_cart,
    get_cart,
    remove_from_cart,
    update_cart_quantity, 
)

>>>>>>> 4fc05c4 (Remove .pyc and __pycache__ from version control and update .gitignore)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
<<<<<<< HEAD
    path('products/stock/update/', update_stock, name='update-stock'),
=======

    path('add-to-cart/', add_to_cart, name='add-to-cart'),  
    path('get-cart/', get_cart, name='get-cart'), 
    path('remove-from-cart/', remove_from_cart, name='remove-from-cart'),
    path('update-cart/', update_cart_quantity, name='update-cart'),
>>>>>>> 4fc05c4 (Remove .pyc and __pycache__ from version control and update .gitignore)
]
