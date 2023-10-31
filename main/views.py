from django.shortcuts import render
from .models import Media

def list_media(request, filter):
    media_list = Media.objects.raw(
        f"""
        SELECT spotify_id, overall_rating
        FROM media
        ORDER BY {filter} DESC
        """
    )

    return render(request, 'main/home.html',
                  {'media_list': media_list,})
