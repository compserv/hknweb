from django import forms
from hknweb.models import User
from hknweb.models import Profile
from .models import Event
from .models import EventType


class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=('%m/%d/%Y %I:%M %p',))
    end_time = forms.DateTimeField(input_formats=('%m/%d/%Y %I:%M %p',))

    class Meta:
        model = Event
        fields = ('name', 'slug', 'location', 'description', 'event_type', 'start_time', 'end_time', 'rsvp_limit')

        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'e.g. <semester>-<name>'}),
        }

        labels = {
            'slug': 'URL-friendly name',
            'rsvp_limit': 'RSVP limit',
        }

class EventUpdateForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=('%m/%d/%Y %I:%M %p',))
    end_time = forms.DateTimeField(input_formats=('%m/%d/%Y %I:%M %p',))

    class Meta:
        model = Event
        fields = ['name', 'slug', 'start_time', 'end_time', 'location', 'event_type',
                  'description', 'rsvp_limit']

        labels = {
            'slug': 'URL-friendly name',
            'rsvp_limit': 'RSVP limit',
        }
