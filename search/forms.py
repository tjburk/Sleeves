from django import forms

class SearchMediaForm(forms.Form):

    ORDER_CHOICES = [
    ('DESC', 'Descending'),
    ('ASC', 'Ascending'),
    ]
    TYPE_CHOICES = [
    ('', 'None'),
    ('track', 'Song'),
    ('album', 'Album'),
    ('podcast', 'Podcast'),
    ('episode', 'Episode'),
    ]

    search_keyword = forms.CharField(label='Search a keyword')
    type = forms.CharField(label='Filter by...', widget=forms.Select(choices=TYPE_CHOICES))
    order = forms.CharField(label='Order by rating...', widget=forms.Select(choices=ORDER_CHOICES))


class SearchUserForm(forms.Form):
    search_keyword = forms.CharField(label='Search a username')