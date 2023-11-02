from django import forms

class FilterMediaForm(forms.Form):
    DATABASE_CHOICES = [
    ('title', 'Title'),
    ('overall_rating', 'Rating'),
    ('length', 'Length')
    ]
    ORDER_CHOICES = [
    ('ASC', 'Ascending'),
    ('DESC', 'Descending'),
    ]

    filter = forms.CharField(label='Order by...', widget=forms.Select(choices=DATABASE_CHOICES))
    order = forms.CharField(label='', widget=forms.Select(choices=ORDER_CHOICES))