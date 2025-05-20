from django.urls import path

# Core account views
from .views import (
    login,
    logout,
    get_current_user,
    csrf_token,
)

# Product-manager–only views
from .product_manager_views import (
    admin_dashboard,
    approve_review,
    disapprove_review,
    add_product,
    update_product,
    remove_product,
    update_stock,
)

urlpatterns = [
    # Authentication
    path("login/",  login,  name="login"),
    path("logout/", logout, name="logout"),
    path("me/",     get_current_user, name="get_current_user"),
    path('csrf-token/', csrf_token, name='csrf_token'),

    # pm endpointleri

    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),

    path("pm/review/<int:review_id>/", approve_review, name="approve_review"),

    path("pm/review/disapprove/<int:review_id>/", disapprove_review, name="disapprove_review"),
    path("admin/products/", add_product, name="add_product"),
    path("admin/products/<int:pk>/", update_product, name="update_product"),
    path("admin/products/<int:pk>/delete/", remove_product, name="remove_product"),
    path("admin/products/<int:pk>/stock/", update_stock, name="update_stock"),

]
    
    

