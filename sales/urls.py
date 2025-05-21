from django.urls import path
from .views import (
    hello_sales, set_price, set_discount, invoices_between, revenue_report, revenue_chart, invoices_pdf
    )

urlpatterns = [
    path("hello/", hello_sales),
    path("products/<int:pk>/price/", set_price),
    path("discounts/", set_discount),
    path("invoices/", invoices_between),
    path("revenue/", revenue_report),
    path("invoices/pdf/", invoices_pdf, name="invoices_pdf"),
    path("revenue/chart/", revenue_chart, name="revenue_chart"),
]
