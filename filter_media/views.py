from django.shortcuts import render
from .models import Media
from .forms import FilterMediaForm

def filter_media(request):
    if request.method == "POST":
        filter_form = FilterMediaForm(request.POST)

        if filter_form.is_valid():
            filter = filter_form.cleaned_data["filter"]
            order = filter_form.cleaned_data["order"]
        
            media_list = Media.objects.raw(
            f"""
            SELECT title, spotify_id, overall_rating
            FROM media NATURAL JOIN spotify
            ORDER BY {filter} {order}
            """
            )
            return render(request, 'main/home.html',
                {'filter_form': filter_form, 'media_list': media_list,})
    else:
        filter_form = FilterMediaForm()

    return render(request, 'main/home.html',
                {'filter_form': filter_form,})
