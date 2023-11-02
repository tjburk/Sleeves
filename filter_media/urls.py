from django.urls import path
from .views import filter_media

urlpatterns = [
    path('', filter_media, name="filter"),
]