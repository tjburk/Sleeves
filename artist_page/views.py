from django.shortcuts import render
from sleeves.models import Artist

def artist_view(request, artist_id):
    artist_object = Artist.objects.raw(
    f"""
    SELECT *
    FROM artist
    WHERE artist_id = '{artist_id}'
    LIMIT 1;
    """
    )[0]

    return render(request, 'artist_page/artist_page.html',
        {'artist': artist_object,})