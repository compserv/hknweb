from django import forms
from .models import ReviewSession


class ReviewSessionForm(forms.ModelForm):

    class Meta:
        model = ReviewSession
        fields = ('name', 'slug', 'location', 'description', 'start_time', 'end_time')

        help_texts = {
            'start_time': 'mm/dd/yyyy hh:mm, 24-hour time',
            'end_time': 'mm/dd/yyyy hh:mm, 24-hour time',
            'slug': 'e.g. <semester>-<name>',
        }

        labels = {
            'slug': 'URL-friendly name',
        }
