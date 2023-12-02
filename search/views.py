from django.shortcuts import render
from sleeves.models import Media, AuthUser
from .forms import SearchMediaForm, SearchUserForm

def search_media(request):
    if request.method == "POST":
        search_form = SearchMediaForm(request.POST)

        if search_form.is_valid():
            search_keyword = search_form.cleaned_data["search_keyword"]
            order = search_form.cleaned_data["order"]
            type = search_form.cleaned_data["type"]
            search_results = None

            if type == "track" or type == "album":
                search_results = Media.objects.raw(
                f"""
                SELECT DISTINCT media.spotify_id, type, media.name, overall_rating, artist_name, album_type, album_art
                FROM media, album NATURAL JOIN artist, song
                WHERE name LIKE '%%{search_keyword}%%' AND type = '{type}'
                AND (spotify_id = album.album_id 
                    OR (spotify_id = song_id AND album.album_id=song.album_id))
                ORDER BY overall_rating {order}
                """
                )
            elif type == "show" or type == "episode":
                search_results = Media.objects.raw(
                f"""
                SELECT DISTINCT media.spotify_id, type, media.name, overall_rating, producer, image
                FROM media, podcast, episode
                WHERE name LIKE '%%{search_keyword}%%' AND type = '{type}'
                AND (spotify_id = podcast.podcast_id 
                    OR (spotify_id = episode_id AND podcast.podcast_id=episode.podcast_id))
                ORDER BY overall_rating {order}
                """
                )         
            
            return render(request, 'search/media.html',
                    {'search_form': search_form, 'search_results': search_results,})
    else:
        search_form = SearchMediaForm()

    return render(request, 'search/media.html',
                {'search_form': search_form,})


def search_user(request):
    if request.method == "POST":
        search_form = SearchUserForm(request.POST)

        if search_form.is_valid():
            search_keyword = search_form.cleaned_data["search_keyword"]

            search_results = AuthUser.objects.raw(
                f"""
                    SELECT *
                    FROM sleeves_user
                    WHERE username LIKE '%%{search_keyword}%%'
                """
            )
            return render(request, 'search/user.html',
                          {'user_form' : search_form, 'user_results' : search_results})
    else:
        search_form = SearchUserForm()

    return render(request, 'search/user.html',
                    {'user_form' : search_form})

