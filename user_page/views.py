from django.shortcuts import render
from sleeves.models import AuthUser, Review
from django.db import connection

def user_page(request, user_id):
    current_user = request.user

    user_reviews = Review.objects.raw(
        f"""
        SELECT title, text, star_rating, auth_user.id, review.auth_id, spotify_id
        FROM auth_user, review 
        WHERE auth_user.id = {user_id}
        AND review.auth_id = {user_id};
        """
    )

    return render(request, 'user_page/user_page.html',
                          {'reviews' : user_reviews})


def delete_review(request, user_id, spotify_id, title):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            DELETE FROM review
            WHERE auth_id = {user_id} AND spotify_id = "{spotify_id}" AND title = "{title}";
            """
        )
    
    return user_page(request, user_id)