from django import forms

class FilterMediaForm(forms.Form):
    DATABASE_CHOICES = [
    ('title', 'title'),
    ('overall_rating', 'overall_rating'),
    ('length', 'length')
    ]
    ORDER_CHOICES = [
    ('ASC', 'ascending'),
    ('DESC', 'descending'),
    ]

    filter = forms.CharField(label='Order by...', widget=forms.Select(choices=DATABASE_CHOICES))
    order = forms.CharField(widget=forms.Select(choices=ORDER_CHOICES))