from django.urls import path
<<<<<<< HEAD

from .views import add_review

urlpatterns = [
    path('add/', add_review, name='add_review'),
]
=======
from .views import submit_review

urlpatterns = [
    path('submit/', submit_review, name='submit_review'),
]
>>>>>>> c5c2500aa43b293b010839f7f5c7a9f7bd1a7009
