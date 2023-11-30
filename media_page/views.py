from django.shortcuts import render
from sleeves.models import Media

def media_view(request, spotify_id):
    media_object = Media.objects.raw(
    f"""
    SELECT *
    FROM media
    WHERE spotify_id = {spotify_id};
    """
    )
    return render(request, 'media_page/media_page.html',
        {'media_object': media_object,})