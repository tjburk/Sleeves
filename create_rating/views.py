from django.shortcuts import render
from sleeves.models import SleevesUser
from .forms import RateForm
from django.db import connection

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

            # Get Spotify ID from URL

            spotify_id = spotify_url.split('/')[4]

            # Insert user into SleevesUser table if it is not already in there
            if get_user(firstname, lastname) is None:
                insert_user(firstname, lastname)
            
            user = get_user(firstname, lastname)

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
            VALUES ('{firstname}', '{lastname}');
            """
        )


def insert_rating(user_id, spotify_id, title, star_rating, text):
    with connection.cursor() as cursor:
        try: 
            cursor.execute(
                f"""
                INSERT INTO review
                VALUES ('{user_id}', '{spotify_id}', '{title}', '{star_rating}', '{text}');
                """
            )
            return True
        # If duplicate rating or something goes wrong
        except:
            return False