from django.urls import path
from accounts.views import signup, login

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('me/', get_current_user, name='get_current_user'),

]
