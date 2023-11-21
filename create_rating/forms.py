from django import forms

class RateForm(forms.Form):
    firstname = forms.CharField(label='First Name', required=True, max_length=25)
    lastname = forms.CharField(label='Last Name', required=True, max_length=25)
    spotify_id = forms.CharField(label='Spotify URL', required=True, max_length=500)
    title = forms.CharField(label='Review Title', required=True, max_length=100)
    star_rating = forms.DecimalField(label='Star Rating', required=True, min_value=1.0, max_value=5.0)
    text = forms.CharField(label="Comment", widget=forms.Textarea)