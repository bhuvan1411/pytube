from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video 
        fields = ['title', 'youtube_url', 'order', 'description', 'thumbnail_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Video title'}),
            'youtube_url': forms.URLInput(attrs={'placeholder': 'YouTube URL'}),
            'order': forms.NumberInput(attrs={'min': 1}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Video description'}),
            'thumbnail_url': forms.URLInput(attrs={'placeholder': 'Thumbnail URL'}),
        }


