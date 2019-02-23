from django import forms
from hknweb.models import User
from hknweb.models import Profile
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'slug', 'location', 'description', 'start_time', 'end_time', 'rsvp_limit')
                  #'markdown', 'event_type', 'view_permission', 'rsvp_type', 'transportation')

        widgets = {
            'start_time': forms.SplitDateTimeWidget(),
            'end_time': forms.SplitDateTimeWidget()
        }

        labels = {
            'start_time': 'Start',
            'end_time': 'End',
        }
