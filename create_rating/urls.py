from django.urls import path
from .views import create_rating

urlpatterns = [
    path('', create_rating, name="create_rating"),
]