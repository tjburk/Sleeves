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
    path('', include('homepage.urls')),
    path('media/', include('media_page.urls')),
    path('artist/', include('artist_page.urls')),
    path('search/', include('search.urls')),
    path('create_rating/', include('create_rating.urls')),
    path('user_profile/', include('user_page.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('sleevesUserAuth.urls'), name='auth')
]
