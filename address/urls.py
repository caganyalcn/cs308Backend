from django.urls import path
from .views import get_addresses, create_address, delete_address

urlpatterns = [
    path('addresses', get_addresses),
    path('addresses', create_address),
    path('addresses/<int:address_id>', delete_address),
]
