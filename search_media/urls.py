from django.urls import path
from .views import search_media, user_search

urlpatterns = [
    path('media/', search_media, name="media"),
    path('user/', user_search, name="user")
]