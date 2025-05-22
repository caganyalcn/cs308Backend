from django.urls import path
from .views import update_order_status, delivery_list, place_order, get_latest_order, get_all_orders_for_user, get_invoice_details, get_invoice_pdf

urlpatterns = [
    path('update-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('delivery-list/', delivery_list, name='delivery_list'),
    path('place/', place_order, name='place_order'),
    path('latest/', get_latest_order, name='latest_order'),
    path('all/', get_all_orders_for_user, name='all_orders'),
    path('invoice/<int:order_id>/', get_invoice_details, name='get_invoice_details'),
    path('invoice/<int:order_id>/pdf/', get_invoice_pdf, name='get_invoice_pdf'),
]

