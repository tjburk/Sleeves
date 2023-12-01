from django.shortcuts import render
from sleeves.models import Media, Album, Song, Artist, Review

def media_view(request, spotify_id):
    media_object = Media.objects.raw(
    f"""
    SELECT *
    FROM media
    WHERE spotify_id = '{spotify_id}'
    LIMIT 1;
    """
    )[0]

    # Set defualts to none
    album_object = None
    song_object = None
    artist_object = None
    
    # Get Song and Album if it's a song
    if media_object.type == "track":
        song_object = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{spotify_id}'
        LIMIT 1;
        """
        )[0]

        album_object = Album.objects.raw(
        f"""
        SELECT *
        FROM album
        WHERE album_id = '{song_object.album_id}'
        LIMIT 1;
        """
        )[0]
    
    # Only get album if it's an album
    elif media_object.type == "album":
        album_object = Album.objects.raw(
        f"""
        SELECT *
        FROM album
        WHERE album_id = '{spotify_id}'
        LIMIT 1;
        """
        )[0]
    
    # If the album was fetched successfully, get the artist
    if(album_object):
        artist_object = Artist.objects.raw(
        f"""
        SELECT *
        FROM artist
        WHERE artist_id = '{album_object.artist_id}'
        LIMIT 1;
        """
        )[0]
    
    reviews = Review.objects.raw(
        f"""
        SELECT *
        FROM review
        WHERE spotify_id = '{spotify_id}'
        """
        )
    
    return render(request, 'media_page/media_page.html',
        {'album': album_object, 'song':song_object, 'artist':artist_object, 'media': media_object, 'reviews':reviews})