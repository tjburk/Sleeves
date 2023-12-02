from django.urls import path
from .views import register_user, user_login


urlpatterns = [
    path('signup', register_user, name="signup"),
    path('login', user_login, name="signup"),
]