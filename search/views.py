from django.shortcuts import render
from sleeves.models import Media, AuthUser
from .forms import SearchMediaForm, SearchUserForm

#Method to search media from the search bar
def search_media(request):
    #Communicates to HTML that this is a POST method
    if request.method == "POST":
        #Processes user responses from Django Form into a format we can plug into SQL queries
        search_form = SearchMediaForm(request.POST)

        #We first have to ensure that all the data inputted is valid to the corresponding object types (string, int, etc.)
        if search_form.is_valid():
            search_keyword = search_form.cleaned_data["search_keyword"]
            order = search_form.cleaned_data["order"]
            type = search_form.cleaned_data["type"]
            search_results = None

            #Albums/tracks and shows/episodes have slightly different collumns in their respected tables, so they require different SQL queries
            if type == "track" or type == "album":
                #Custom SQL query to retrieve items from the data base
                #Explanation: we are fetching the distinct spotify_id, object type, name, overall rating, artist name, album type, and art
                #We natural join album and artist on the albums artist_id and the artists spotify_id
                #To ensure our search is accurate, we check name, type, and that the corresponding primary keys match
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
                #Custom SQL query to retrieve items from the data base
                #Explanation: we are fetching the distinct spotify_id, object type, overall rating, the shows producer, and its spotify image
                #This search does not require a natural join, since podcasts are singular objects while artists can have multiple albums
                #To ensure search is accurate, we just need to check that all the ids match with one another
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
            #Once SQL query is completed, the results are returned to our media.html so they can be rendered on the frontend
            return render(request, 'search/media.html',
                    {'search_form': search_form, 'search_results': search_results,})
    else:
        search_form = SearchMediaForm()

    #If search is not valid, we just return an empty search, which will just return the highest rated objects
    return render(request, 'search/media.html',
                {'search_form': search_form,})

#Method to search users
def search_user(request):
    #Communicates to HTML that this is a POST method
    if request.method == "POST":
         #Processes user responses from Django Form into a format we can plug into SQL queries
        search_form = SearchUserForm(request.POST)

        if search_form.is_valid():
            search_keyword = search_form.cleaned_data["search_keyword"]

            #Explanation: returns all users that are similar to the name returned
            #This query is much simpler than the album/podcast ones, as we only need to check the username
            search_results = AuthUser.objects.raw(
                f"""
                    SELECT *
                    FROM auth_user
                    WHERE username LIKE '%%{search_keyword}%%'
                """
            )
            #Returns data fetched from SQL query to user.html, where it will be rendered on the web page
            return render(request, 'search/user.html',
                          {'user_form' : search_form, 'user_results' : search_results})
    else:
        search_form = SearchUserForm()

    #Same as album/podcast search, if search is invalid, will return list of users alphabetically
    return render(request, 'search/user.html',
                    {'user_form' : search_form})

