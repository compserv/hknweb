from django import forms
from hknweb.models import User
from hknweb.models import Profile
from .models import Event
from .models import EventType


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'slug', 'location', 'description', 'event_type', 'start_time', 'end_time', 'rsvp_limit')
                  # 'markdown', 'event_type', 'view_permission', 'rsvp_type', 'transportation')

        # this makes formatting easier, but it shows as MM/DD/YYY HH:MM AM/PM which apparently is not valid for the datetimefield :(
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'e.g. <semester>-<name>'}),
            # 'start_time': forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
            # 'end_time': forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
        }
        help_texts = {
            'start_time': 'mm/dd/yyyy hh:mm, 24-hour time',
            'end_time': 'mm/dd/yyyy hh:mm, 24-hour time',
        }

        labels = {
            'slug': 'URL-friendly name',
            'rsvp_limit': 'RSVP limit',
        }
