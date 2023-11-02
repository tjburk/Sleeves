from django.urls import path
from .views import search_media

urlpatterns = [
    path('', search_media, name="search"),
]