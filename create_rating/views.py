from django.shortcuts import render
from sleeves.models import SleevesUser, Media, Album, Artist, Genre, Podcast
from .forms import RateForm
from django.db import connection
from django.conf import settings

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=settings.SPOTIPY_CLIENT_ID, client_secret=settings.SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def create_rating(request):
    # Process form
    if request.method == "POST":
        rate_form = RateForm(request.POST)

        if rate_form.is_valid():
            # Get data from form
            firstname = rate_form.cleaned_data["firstname"]
            lastname = rate_form.cleaned_data["lastname"]
            spotify_url = rate_form.cleaned_data["spotify_url"]
            title = rate_form.cleaned_data["title"]
            star_rating = rate_form.cleaned_data["star_rating"]
            text = rate_form.cleaned_data["text"]

            # Get the spotify ID from the URL
            spotify_type = spotify_url.split('/')[3]
            spotify_id = spotify_url.split('/')[4].split('?')[0]
            print(spotify_id)

            # Insert user into SleevesUser table if it is not already in there
            if get_user(firstname, lastname) is None:
                insert_user(firstname, lastname)
            
            user = get_user(firstname, lastname)
            
            # Insert media into Media table if it is not already in there
            if get_media(spotify_id) is None:
                insert_media(spotify_id, spotify_type, star_rating)

            # Then, insert rating into the Rating table
            success = insert_rating(user.user_id, spotify_id, title, star_rating, text)

            return render(request, 'create_rating/create_rating.html',
                {'rate_form':rate_form, "user":user, "success":success, "init":True})
    else:
        rate_form = RateForm()

    return render(request, 'create_rating/create_rating.html', 
                {'rate_form': rate_form, "init":False})


def get_user(firstname, lastname):
    # If user exists, return it
    try:
        user = SleevesUser.objects.raw(
            f"""
            SELECT *
            FROM sleeves_user
            WHERE first = '{firstname}' AND last = '{lastname}'
            LIMIT 1;
            """
        )[0]
    # If it doesn't return None
    except:
        user = None
    
    return user


def insert_user(firstname, lastname):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO sleeves_user (first, last)
            VALUES ("{firstname}", "{lastname}");
            """
        )


def insert_rating(user_id, spotify_id, title, star_rating, text):
    print("rating: " + str(user_id) + " " + spotify_id + " " + title)
    with connection.cursor() as cursor:
        try: 
            cursor.execute(
                f"""
                INSERT INTO review
                VALUES ({user_id}, "{spotify_id}", "{title}", {star_rating}, "{text}");
                """
            )
            return True
        # If duplicate rating or something goes wrong
        except:
            return False


def get_media(spotify_id):
    # If media exists, return it
    try:
        media = Media.objects.raw(
            f"""
            SELECT *
            FROM media
            WHERE spotify_id = '{spotify_id}'
            LIMIT 1;
            """
        )[0]
        
    # If it doesn't return None
    except:
        media = None
    
    return media

def insert_media(spotify_id, spotify_type, star_rating):
    media = None

    # If star_rating is nothing
    if not star_rating:
        star_rating = "NULL"

    # Check for what type the media is
    if spotify_type == "album":
        media = spotify.album(spotify_id)
    elif spotify_type == "track":
        media = spotify.track(spotify_id)
    elif spotify_type == "episode":
        media = spotify.episode(spotify_id)
    elif spotify_type == "show":
        media = spotify.show(spotify_id)
    
    # If no rating previously, insert into media with only rating as overall rating
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO media (spotify_id, overall_rating, name, type)
            VALUES ("{spotify_id}", {star_rating}, "{media["name"]}", "{media["type"]}");
            """
        )
    if spotify_type == "track":
        if not get_album(media["album"]["id"]):
            insert_media(media["album"]["id"], "album", None) # recursive call with no rating!
        insert_song(media)
    elif spotify_type == "album":
        insert_album(media)
    elif spotify_type == "episode":
        if not get_podcast(media["show"]["id"]):
            insert_media(media["show"]["id"], "show", None) # recursive call with no rating!
        insert_episode(media)
    elif spotify_type == "show":
        insert_podcast(media)


def get_album(album_id):
    # If album exists, return it
    try:
        album = Album.objects.raw(
            f"""
            SELECT *
            FROM album
            WHERE album_id = '{album_id}'
            LIMIT 1;
            """
        )[0]
        
    # If it doesn't return None
    except:
        album = None
    
    return album


def insert_album(album):
    # Get params for SQL
    album_id = album["id"]
    album_type = album["album_type"]
    album_art = album["images"][0]["url"]
    record_label = album["label"]
    artist_id = album["artists"][0]["id"]

    # Add artist if not already in database
    if not get_artist(artist_id):
        insert_artist(artist_id)

    # Insert into album table
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO album (album_id, album_type, album_art, record_label, artist_id)
            VALUES ("{album_id}", "{album_type}", "{album_art}", "{record_label}", "{artist_id}");
            """
        )
    
    # Insert genre if not already in database
    genre_name = album["genres"]
    genre = get_genre(genre_name)
    if genre is None:
        insert_genre(genre_name)
    genre = get_genre(genre_name)
    insert_album_has_genre(album_id, genre.genre_id)


def get_genre(genre_name):
    # If album exists, return it
    try:
        genre = Genre.objects.raw(
            f"""
            SELECT *
            FROM genre
            WHERE genre_name = '{genre_name}'
            LIMIT 1;
            """
        )[0]
        
    # If it doesn't return None
    except:
        genre = None
    
    return genre


def insert_genre(genre_name):
    # Insert into genre table
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO genre (genre_name)
            VALUES ("{genre_name}");
            """
        )

def insert_album_has_genre(album_id, genre_id):
    # Insert into album_has_genre table
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO album_has_genre (genre_id, album_id)
            VALUES ({genre_id}, "{album_id}");
            """
        )


def get_artist(artist_id):
    try:
        artist = Artist.objects.raw(
            f"""
            SELECT *
            FROM artist
            WHERE artist_id = '{artist_id}'
            LIMIT 1;
            """
        )[0]
        
    # If it doesn't return None
    except:
        artist = None
    
    return artist


def insert_artist(artist_id):
    # Get params for SQL
    artist = spotify.artist(artist_id)
    artist_name = artist["name"]
    image = artist["images"][0]["url"]

    # Insert into table
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO artist (artist_id, artist_name, image)
            VALUES ("{artist_id}", "{artist_name}", "{image}");
            """
        )


def insert_song(song):
    # Get params for SQL
    song_id = song["id"]
    audio_analysis = spotify.audio_analysis(song_id)
    tempo = audio_analysis["track"]["tempo"]
    key = audio_analysis["track"]["key"]
    loudness = audio_analysis["track"]["loudness"]
    album_id = song["album"]["id"]
    length = song["duration_ms"]

    # Insert into table
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO song (song_id, tempo, song_key, loudness, album_id, length)
            VALUES ("{song_id}", {tempo}, "{key}", {loudness}, "{album_id}", {length});
            """
        )

def insert_episode(episode):
    # Get params for SQL
    episode_id = episode["id"]
    release_date = episode["release_date"]
    synopsis = episode["description"]
    podcast_id = episode["show"]["id"]
    length = episode["duration_ms"]

    # Insert into table
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO episode (episode_id, release_date, synopsis, podcast_id, length)
            VALUES ("{episode_id}", "{release_date}", "{synopsis}", "{podcast_id}", {length});
            """
        )

def get_podcast(podcast_id):
    # If album exists, return it
    try:
        podcast = Podcast.objects.raw(
            f"""
            SELECT *
            FROM podcast
            WHERE podcast_id = '{podcast_id}'
            LIMIT 1;
            """
        )[0]
        
    # If it doesn't return None
    except:
        podcast = None
    
    return podcast

def insert_podcast(podcast):
    # Get params for SQL
    podcast_id = podcast["id"]
    description = podcast["description"]
    producer = podcast["publisher"]
    image = podcast["images"][0]["url"]

    # Insert into table
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO podcast (podcast_id, description, producer, image)
            VALUES ("{podcast_id}", "{description}", "{producer}", "{image}");
            """
        )