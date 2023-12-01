from django.shortcuts import render
from sleeves.models import Media, Song, Album, Review, SleevesUser, Artist

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

    # Get random review
    review = Review.objects.raw(
        f"""
        SELECT DISTINCT review.spotify_id, review.title, review.user_id, review.star_rating, review.text, album_art, artist_id
        FROM review, album NATURAL JOIN song AS albumsong
        WHERE review.spotify_id = albumsong.album_id OR review.spotify_id = albumsong.song_id
        ORDER BY RAND()
        LIMIT 1;
        """
    )[0]

    review_media = Media.objects.raw(
        f"""
        SELECT *
        FROM media
        WHERE spotify_id = '{review.spotify_id}';
        """
    )[0]

    review_user = SleevesUser.objects.raw(
        f"""
        SELECT *
        FROM sleeves_user
        WHERE id = {review.user_id};
        """
    )[0]

    review_artist = Artist.objects.raw(
        f"""
        SELECT *
        FROM artist
        WHERE artist_id = '{review.artist_id}';
        """
    )[0]
    

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
                                                  "bestestalbums":bestest_albums ,
                                                  "review":review,
                                                  "review_media":review_media,
                                                  "review_user":review_user,
                                                  "review_artist":review_artist})