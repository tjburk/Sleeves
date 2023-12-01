from django.urls import path
from .views import search_media, search_user

urlpatterns = [
    path('media/', search_media, name="search_media"),
    path('user/', search_user, name="search_user")
]