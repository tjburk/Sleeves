from django.shortcuts import render
from sleeves.models import Media, SleevesUser
from .forms import SearchMediaForm

def search_media(request):
    if request.method == "POST":
        search_form = SearchMediaForm(request.POST)

        if search_form.is_valid():
            search_keyword = search_form.cleaned_data["search_keyword"]

            search_results = Media.objects.raw(
            f"""
            SELECT name, spotify_id
            FROM media
            WHERE name LIKE '%%{search_keyword}%%';
            """
            )
            return render(request, 'search_media/search.html',
                {'search_form': search_form, 'search_results': search_results,})
    else:
        search_form = SearchMediaForm()

    return render(request, 'search_media/search.html',
                {'search_form': search_form,})

def view_reviews(request):
    if request.method == "POST":
        search_form = SearchMediaForm(request.POST)

        if search_form.is_valid():
            search_keyword = search_form.cleaned_data["search_keyword"]

            search_results = Media.objects.raw(
                f"""
                    SELECT DISTINCT first, last , review.spotify_id, name, title, star_rating, text
                    FROM review NATURAL JOIN sleeves_user, media
                    WHERE name LIKE '%%{search_keyword}%%' and review.spotify_id = media.spotify_id
                """
            )
            return render(request, 'search_media/review.html',
                          {'review_form' : search_form, 'review_results' : search_results})
    else:
        search_form = SearchMediaForm()
        search_results = Media.objects.raw(
                f"""
                    SELECT DISTINCT first, last , review.spotify_id, name, title, star_rating, text
                    FROM review NATURAL JOIN sleeves_user, media    
                    WHERE review.spotify_id = media.spotify_id
                    ORDER BY star_rating DESC
                """
            )

    return render(request, 'search_media/review.html',
                          {'review_form' : search_form, 'review_results' : search_results})


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