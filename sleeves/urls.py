"""sleeves URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('media/', include('media_page.urls'), name="media"),
    path('search/', include('search_media.urls'), name="search"),
    path('create_rating/', include('create_rating.urls'), name="create_rating"),
    path('user_profile/', include('pages.urls'), name="user_profile"),
    path('', include('homepage.urls'), name="home"),
    path('admin/', admin.site.urls),
]
