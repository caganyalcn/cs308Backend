from django.urls import path
from .views import test_mail_view, update_order_status, delivery_list, place_order  

urlpatterns = [
    path('test-mail/', test_mail_view),
    path('update-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('delivery-list/', delivery_list, name='delivery_list'),
    path('place/', place_order, name='place_order'),  
]

