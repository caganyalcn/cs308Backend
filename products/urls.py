from django.urls import path

from .views import (
    ProductListView, 
    ProductDetailView, 
    add_to_cart,
    get_cart,
    remove_from_cart,
    update_cart_quantity, 
    create_product,
    update_product,
    delete_product,
    list_categories,
    create_category,
    update_category,
    delete_category,
    update_stock,
    set_product_price,
    apply_discount,
    calculate_revenue_loss,

)


urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', create_product, name='create_product'),
    path('products/<int:product_id>/update/', update_product, name='update_product'),
    path('products/<int:product_id>/delete/', delete_product, name='delete_product'),

    path('add-to-cart/', add_to_cart, name='add-to-cart'),  
    path('get-cart/', get_cart, name='get-cart'), 
    path('remove-from-cart/', remove_from_cart, name='remove-from-cart'),
    path('update-cart/', update_cart_quantity, name='update-cart'),
    
    # Category Management
    path('categories/', list_categories, name='list_categories'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/<int:category_id>/update/', update_category, name='update_category'),
    path('categories/<int:category_id>/delete/', delete_category, name='delete_category'),

    path('sales/set-price/', set_product_price, name='set_price'),
    path('sales/apply-discount/', apply_discount, name='apply_discount'),
    #path('sales/notify-wishlist/', notify_wishlist, name='notify_wishlist'),
    path('sales/revenue-loss/', calculate_revenue_loss, name='revenue_loss'),
]
