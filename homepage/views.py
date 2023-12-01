from django.shortcuts import render
from sleeves.models import Media, Song, Album

def home(request):
    top5media = Media.objects.raw(
        f"""
        SELECT *
        FROM media
        WHERE type = "track"
        ORDER BY overall_rating DESC
        LIMIT 5;
        """
    )

    song1 = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{top5media[0].spotify_id}' 
        """
    )[0]
    album1 = Album.objects.raw(
        f"""
        SELECT *
        FROM album
        WHERE album_id = '{song1.album_id}' 
        """
    )[0]
    song2 = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{top5media[1].spotify_id}' 
        """
    )[0]
    album2 = Album.objects.raw(
        f"""
        SELECT *
        FROM album
        WHERE album_id = '{song2.album_id}' 
        """
    )[0]
    song3 = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{top5media[2].spotify_id}' 
        """
    )[0]
    album3 = Album.objects.raw(
        f"""
        SELECT *
        FROM album
        WHERE album_id = '{song3.album_id}' 
        """
    )[0]
    song4 = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{top5media[3].spotify_id}' 
        """
    )[0]
    album4 = Album.objects.raw(
        f"""
        SELECT *
        FROM album
        WHERE album_id = '{song4.album_id}' 
        """
    )[0]
    song5 = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{top5media[4].spotify_id}' 
        """
    )[0]
    album5 = Album.objects.raw(
        f"""
        SELECT *
        FROM album
        WHERE album_id = '{song5.album_id}' 
        """
    )[0]
    top5songs = [song1, song2, song3, song4, song5]
    top5songs_albums = [album1, album2, album3, album4, album5]

    bestest_albums = Album.objects.raw(
        """
        SELECT spotify_id, album_id, name, album_art, overall_rating
        FROM media, album
        WHERE type = "album" AND media.spotify_id = album.album_id
        ORDER BY overall_rating DESC
        LIMIT 5;
        """
    )

    return render(request, "homepage/home.html", {"top5media": top5media, 
                                                  "top5songs":top5songs, 
                                                  "top5songs_albums":top5songs_albums,
                                                  "bestestalbums":bestest_albums })