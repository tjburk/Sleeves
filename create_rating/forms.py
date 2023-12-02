from django import forms

class RateForm(forms.Form):
    spotify_url = forms.CharField(label='Spotify URL', required=True, max_length=500)
    title = forms.CharField(label='Review Title', required=True, max_length=100)
    star_rating = forms.DecimalField(label='Star Rating', required=True, min_value=1.0, max_value=5.0)
    text = forms.CharField(label="Comment", widget=forms.Textarea)