from django.urls import path
from .views import update_order_status, delivery_list, place_order, get_latest_order, get_all_orders_for_user, get_invoice_details, get_invoice_pdf, orders_by_date_range, calculate_revenue, cancel_order, initiate_refund_request, refund_waiting_orders

urlpatterns = [
    path('update-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('delivery-list/', delivery_list, name='delivery_list'),
    path('place/', place_order, name='place_order'),
    path('latest/', get_latest_order, name='latest_order'),
    path('all/', get_all_orders_for_user, name='all_orders'),
    path('invoice/<int:order_id>/', get_invoice_details, name='get_invoice_details'),
    path('invoice/<int:order_id>/pdf/', get_invoice_pdf, name='get_invoice_pdf'),
    path('by-date-range/', orders_by_date_range, name='orders_by_date_range'),
    path('calculate-revenue/', calculate_revenue, name='calculate_revenue'),
    path('<int:order_id>/cancel/', cancel_order, name='cancel_order'),
    path('<int:order_id>/refund-request/', initiate_refund_request, name='initiate_refund_request'),
    path('refund-waiting/', refund_waiting_orders, name='refund_waiting_orders'),
]

