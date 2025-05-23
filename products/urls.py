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
    add_to_favorites,
    remove_from_favorites,
    get_favorites,
    update_product_price,
    discount_product,  # added discount view
    save_credit_card_details, # Import the new view
)


urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', create_product, name='create_product'),
    path('products/<int:product_id>/update/', update_product, name='update_product'),
    path('products/<int:product_id>/delete/', delete_product, name='delete_product'),
    path('products/update_price/<int:product_id>/', update_product_price, name='update_product_price'),
    path('products/<int:product_id>/discount/', discount_product, name='discount_product'),  # discount route

    path('add-to-cart/', add_to_cart, name='add-to-cart'),  
    path('get-cart/', get_cart, name='get-cart'), 
    path('remove-from-cart/', remove_from_cart, name='remove-from-cart'),
    path('update-cart/', update_cart_quantity, name='update-cart'),

    # Favorite endpoints
    path('favorites/add/', add_to_favorites, name='add-to-favorites'),
    path('favorites/remove/', remove_from_favorites, name='remove-from-favorites'),
    path('favorites/', get_favorites, name='get-favorites'),

    # Category Management
    path('categories/', list_categories, name='list_categories'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/<int:category_id>/update/', update_category, name='update_category'),
    path('categories/<int:category_id>/delete/', delete_category, name='delete_category'),

    # Credit Card Saving during Purchase
    path('save-credit-card-details/', save_credit_card_details, name='save_credit_card_details'),
]
