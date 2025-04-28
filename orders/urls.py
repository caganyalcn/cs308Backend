from django.urls import path
from .views import update_order_status, delivery_list, place_order, get_latest_order

urlpatterns = [
    path('update-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('delivery-list/', delivery_list, name='delivery_list'),
    path('place/', place_order, name='place_order'),
    path('latest/', get_latest_order, name='latest_order'),
]

