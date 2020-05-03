from django import forms
from hknweb.models import User
from hknweb.models import Profile
from .models import Event
from .models import EventType


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'slug', 'location', 'description', 'event_type', 'start_time', 'end_time', 'rsvp_limit')

        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'e.g. <semester>-<name>'}),
            'start_time': forms.widgets.DateTimeInput(format='%d/%m/%Y %H:%M'),
            'end_time': forms.widgets.DateTimeInput(format='%d/%m/%Y %H:%M'),
        }

        labels = {
            'slug': 'URL-friendly name',
            'rsvp_limit': 'RSVP limit',
        }
