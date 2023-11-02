from django.shortcuts import render
from sleeves.models import Media

def search_media(request):
    return render(request, "search_media/search.html")