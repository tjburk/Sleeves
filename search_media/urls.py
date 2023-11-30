from django.urls import path
from .views import search_media, view_reviews, user_search

urlpatterns = [
    path('review/', view_reviews, name="review"),
    path('media/', search_media, name="search"),
    path('user/', user_search, name="user")
]