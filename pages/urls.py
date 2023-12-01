from django.urls import path
from .views import user_page

urlpatterns = [
    path('<user_id>', user_page, name="user"),
]