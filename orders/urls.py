from django.urls import path
from .views import test_mail_view

urlpatterns = [
    path('test-mail/', test_mail_view),
]

from django.urls import path
from .views import update_order_status

urlpatterns = [
    path('update-status/<int:order_id>/', update_order_status, name='update_order_status'),
]
from .views import delivery_list

urlpatterns += [
    path('delivery-list/', delivery_list, name='delivery_list'),
]
