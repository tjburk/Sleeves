from django.urls import path
from media_page.views import media_view


urlpatterns = [
    path('<spotify_id>', media_view, name="media_page"),
]
