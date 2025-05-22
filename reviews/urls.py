from django.urls import path
from .views import add_review, get_product_reviews, get_my_reviews, list_all_reviews, update_review_approval

urlpatterns = [
    path('add/', add_review, name='add_review'),
    path('product/<int:product_id>/', get_product_reviews, name='product_reviews'),
    path('my-reviews/', get_my_reviews, name='my_reviews'),
    path('all/', list_all_reviews, name='list_all_reviews'),
    path('<int:review_id>/update-approval/', update_review_approval, name='update_review_approval'),
]
