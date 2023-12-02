from django.urls import path
from artist_page.views import artist_view


urlpatterns = [
    path('<artist_id>', artist_view, name="artist_page"),
]
