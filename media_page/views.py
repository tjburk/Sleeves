from django.shortcuts import render
from sleeves.models import Media, Album, Song, Artist, Review, Podcast, Episode

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
    podcast_object = None
    episode_object = None
    artist_object = None
    song_key = None
    
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

        # get song key
        key_dict = {"1": "C", "2": "C#", "3": "D", "4": "D#", "5": "E", "6":"F", "7":"F#", "8":"G", "9":"G#", "10":"A", "11":"A#", "12":"B"}
        song_key = key_dict[song_object.song_key]
    
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

    # Get Podcast and Episode if it's an episode
    if media_object.type == "episode":
        episode_object = Episode.objects.raw(
        f"""
        SELECT *
        FROM episode
        WHERE episode_id = '{spotify_id}'
        LIMIT 1;
        """
        )[0]

        podcast_object = Podcast.objects.raw(
        f"""
        SELECT *
        FROM podcast
        WHERE podcast_id = '{episode_object.podcast_id}'
        LIMIT 1;
        """
        )[0]
    
    # Only get podcast if it's an podcast
    elif media_object.type == "show":
        podcast_object = Podcast.objects.raw(
        f"""
        SELECT *
        FROM podcast
        WHERE podcast_id = '{spotify_id}'
        LIMIT 1;
        """
        )[0]
    
    # get reviews
    reviews = Review.objects.raw(
        f"""
        SELECT *
        FROM review
        WHERE spotify_id = '{spotify_id}'
        """
        )
    
    return render(request, 'media_page/media_page.html',
        {'album': album_object, 'song':song_object, 'song_key':song_key, 'podcast': podcast_object, 'episode':episode_object, 'artist':artist_object, 'media': media_object, 'reviews':reviews})