from django.shortcuts import render
from sleeves.models import SleevesUser, Review
from django.db import connection

def user_page(request, user_id):
    user_object  = SleevesUser.objects.raw(
    f"""
    SELECT *
    FROM sleeves_user
    WHERE id = '{user_id}'
    """
    )[0]

    user_reviews = Review.objects.raw(
        f"""
        SELECT title, text, star_rating, sleeves_user.id, review.user_id, spotify_id
        FROM sleeves_user, review 
        WHERE sleeves_user.id = {user_id}
        AND review.user_id = {user_id};
        """
    )

    return render(request, 'user_page/user_page.html',
                          {'user' : user_object, 'reviews' : user_reviews})


def delete_review(request, user_id, spotify_id, title):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            DELETE FROM review
            WHERE user_id = {user_id} AND spotify_id = "{spotify_id}" AND title = "{title}";
            """
        )
    
    return user_page(request, user_id)