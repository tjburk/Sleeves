from django.urls import path
from .views import user_page, delete_review


urlpatterns = [
    path('<user_id>', user_page, name="user_page"),
    path('delete/<user_id>/<spotify_id>/<title>', delete_review, name="delete_review"),
]