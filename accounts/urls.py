from django.urls import path

from accounts.views import login, get_current_user, logout
from accounts.admin_views import admin_dashboard, approve_review


urlpatterns = [
    
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('me/', get_current_user, name='get_current_user'),

    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/approve-review/<int:review_id>/', approve_review, name='approve_review'),

]
