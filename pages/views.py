from django.shortcuts import render
from sleeves.models import SleevesUser, Review

# Create your views here.
def user_page(request, user_id):
    user_object  = SleevesUser.objects.raw(
    f"""
    SELECT *
    FROM sleeves_user
    WHERE user_id = '{user_id}'
    """
    )[0]

    user_reviews = Review.objects.raw(
        f"""
        SELECT title, text, star_rating, sleeves_user.user_id 
        FROM sleeves_user, review 
        WHERE sleeves_user.user_id = '{user_id}'
        AND review.user_id = '{user_id}';
        """
    )


    return render(request, 'pages/user.html',
                          {'user' : user_object, 'reviews' : user_reviews})

    