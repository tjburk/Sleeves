from django.shortcuts import render
from sleeves.models import SleevesUser, Review

# Create your views here.
def user_page(request, user_id):
    user_object  = SleevesUser.objects.raw(
    f"""
    SELECT *
    FROM auth_user
    WHERE id = '{user_id}'
    """
    )[0]

    user_reviews = Review.objects.raw(
        f"""
        SELECT title, text, star_rating, id
        FROM auth_user, review 
        WHERE id = '{user_id}'
        AND review.auth_id = '{user_id}';
        """
    )


    return render(request, 'pages/user.html',
                          {'user' : user_object, 'reviews' : user_reviews})

    