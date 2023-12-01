from django.shortcuts import render
from sleeves.models import Media, Song

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
    song2 = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{top5media[1].spotify_id}' 
        """
    )[0]
    song3 = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{top5media[2].spotify_id}' 
        """
    )[0]
    song4 = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{top5media[3].spotify_id}' 
        """
    )[0]
    song5 = Song.objects.raw(
        f"""
        SELECT *
        FROM song
        WHERE song_id = '{top5media[4].spotify_id}' 
        """
    )[0]
    top5songs = [song1, song2, song3, song4, song5]

    return render(request, "homepage/home.html", {"top5media": top5media, "top5songs":top5songs})