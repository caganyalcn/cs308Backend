from django.urls import path
from .views import hello_sales, set_price, set_discount, invoices_between, revenue_report

urlpatterns = [
    path("hello/", hello_sales),
    path("products/<int:pk>/price/", set_price),
    path("discounts/", set_discount),
    path("invoices/", invoices_between),
    path("revenue/", revenue_report),
]
