from django.shortcuts import render
from sleeves.models import Media, SleevesUser
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from sleeves.models import Media, Artist
from .forms import SearchMediaForm

def search_media(request):
    if request.method == "POST":
        search_form = SearchMediaForm(request.POST)

        if search_form.is_valid():
            search_keyword = search_form.cleaned_data["search_keyword"]
            filter = search_form.cleaned_data["filter"]
            order = search_form.cleaned_data["order"]

            search_results = Media.objects.raw(
            f"""
            SELECT DISTINCT media.spotify_id, type, media.name, overall_rating, artist_name, album_type, album_art
            FROM media, album NATURAL JOIN artist, song 
            WHERE name LIKE '%%{search_keyword}%%'
            ORDER BY {filter} {order}
            AND (spotify_id = album.album_id 
                OR (spotify_id = song_id AND album.album_id=song.album_id))
            ORDER BY {filter} {order}
            """
            )
            return render(request, 'search_media/media.html',
                {'search_form': search_form, 'search_results': search_results,})
    else:
        search_form = SearchMediaForm()
    """
        OR spotify_id = podcast.podcast_id 
                OR (spotify_id = episode_id AND episode.podcast_id = episode.episode_id)

                for when we want podcasts
    """

    return render(request, 'search_media/media.html',
                {'search_form': search_form,})

# def view_reviews(request):
#     if request.method == "POST":
#         search_form = SearchMediaForm(request.POST)

#         if search_form.is_valid():
#             search_keyword = search_form.cleaned_data["search_keyword"]

#             search_results = Media.objects.raw(
#                 f"""
#                     SELECT DISTINCT first, last , review.spotify_id, name, title, star_rating, text
#                     FROM review NATURAL JOIN sleeves_user, media
#                     WHERE name LIKE '%%{search_keyword}%%' and review.spotify_id = media.spotify_id
#                 """
#             )
#             return render(request, 'search_media/review.html',
#                           {'review_form' : search_form, 'review_results' : search_results})
#     else:
#         search_form = SearchMediaForm()
#         search_results = Media.objects.raw(
#                 f"""
#                     SELECT DISTINCT first, last , review.spotify_id, name, title, star_rating, text
#                     FROM review NATURAL JOIN sleeves_user, media    
#                     WHERE review.spotify_id = media.spotify_id
#                     ORDER BY star_rating DESC
#                 """
#             )

#     return render(request, 'search_media/review.html',
#                           {'review_form' : search_form, 'review_results' : search_results})


def user_search(request):
    if request.method == "POST":
        search_form = SearchMediaForm(request.POST)

        if search_form.is_valid():
            search_keyword = search_form.cleaned_data["search_keyword"]

            search_results = SleevesUser.objects.raw(
                f"""
                    SELECT user_id, first, last
                    FROM sleeves_user
                    WHERE CONCAT(first,last) LIKE '%%{search_keyword}%%'
                    OR user_id LIKE '%%{search_keyword}%%'
                    OR first LIKE '%%{search_keyword}%%'
                    OR last LIKE '%%{search_keyword}%%'
                """
            )
            return render(request, 'search_media/user.html',
                          {'user_form' : search_form, 'user_results' : search_results})
    else:
        search_form = SearchMediaForm()
        search_results = SleevesUser.objects.raw(
                f"""
                    SELECT user_id, first, last 
                    FROM sleeves_user
                """ 
            )

        return render(request, 'search_media/user.html',
                            {'user_form' : search_form, 'user_results' : search_results})
    return render(request, 'search_media/search.html',
                {'search_form': search_form,})

