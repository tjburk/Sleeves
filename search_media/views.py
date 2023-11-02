from django.shortcuts import render
from sleeves.models import Media
from .forms import SearchMediaForm

def search_media(request):
    if request.method == "POST":
        search_form = SearchMediaForm(request.POST)

        if search_form.is_valid():
            search_keyword = search_form.cleaned_data["search_keyword"]

            search_results = Media.objects.raw(
            f"""
            SELECT title, spotify_id
            FROM media NATURAL JOIN spotify
            WHERE title LIKE '%%{search_keyword}%%';
            """
            )
            return render(request, 'search_media/search.html',
                {'search_form': search_form, 'search_results': search_results,})
    else:
        search_form = SearchMediaForm()

    return render(request, 'search_media/search.html',
                {'search_form': search_form,})