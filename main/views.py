from django.shortcuts import render
from .models import Artist

def all_artists(request):
    artist_list = Artist.objects.all()
    return render(request, 'main/home.html',
                  {'artist_list': artist_list,})
