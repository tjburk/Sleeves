from django import forms

class SearchMediaForm(forms.Form):

    DATABASE_CHOICES = [
    ('name', 'Title'),
    ('overall_rating', 'Rating'),
    ('length', 'Length')
    ]
    ORDER_CHOICES = [
    ('ASC', 'Ascending'),
    ('DESC', 'Descending'),
    ]

    search_keyword = forms.CharField(label='Search a keyword')
    filter = forms.CharField(label='Order by...', widget=forms.Select(choices=DATABASE_CHOICES))
    order = forms.CharField(label='', widget=forms.Select(choices=ORDER_CHOICES))


class SearchUserForm(forms.Form):
    search_keyword = forms.CharField(label='Search For a User')