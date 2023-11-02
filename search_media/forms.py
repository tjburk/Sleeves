from django import forms

class SearchMediaForm(forms.Form):
    search_keyword = forms.CharField(label='Search a keyword')