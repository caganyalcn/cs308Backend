from django.urls import path
from .views import add_review, get_product_reviews, get_my_reviews, pending_reviews, approve_comment

urlpatterns = [
    path('add/', add_review, name='add_review'),
    path('product/<int:product_id>/', get_product_reviews, name='product_reviews'),
    path('my-reviews/', get_my_reviews, name='my_reviews'),
    path('pending/', pending_reviews, name='pending_reviews'),
    path('<int:pk>/approve/', approve_comment, name='approve_review'),
]
