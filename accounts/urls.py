from django.urls import path

from accounts.views import signup, login, get_current_user, logout


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('me/', get_current_user, name='get_current_user'),
]
