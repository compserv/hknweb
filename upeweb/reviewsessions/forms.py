from django import forms
from .models import ReviewSession


class ReviewSessionForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=('%m/%d/%Y %I:%M %p',))
    end_time = forms.DateTimeField(input_formats=('%m/%d/%Y %I:%M %p',))
  
    class Meta:
        model = ReviewSession
        fields = ('name', 'slug', 'location', 'description', 'start_time', 'end_time')

        help_texts = {
            'start_time': 'mm/dd/yyyy hh:mm, 24-hour time',
            'end_time': 'mm/dd/yyyy hh:mm, 24-hour time',
            'slug': 'e.g. <semester>-<name>',
        }

        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'e.g. <semester>-<name>'}),
        }

        labels = {
            'slug': 'URL-friendly name',
        }

class ReviewSessionUpdateForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=('%m/%d/%Y %I:%M %p',))
    end_time = forms.DateTimeField(input_formats=('%m/%d/%Y %I:%M %p',))

    class Meta:
        model = ReviewSession
        fields = ['name', 'slug', 'start_time', 'end_time', 'location', 'description']

        labels = {
            'slug': 'URL-friendly name',
        }