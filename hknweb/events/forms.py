from django import forms
from hknweb.models import User
from hknweb.models import Profile
from .models import Event
from django.contrib.admin import widgets


class EventForm(forms.ModelForm):

    # start_date = forms.DateTimeField(
    #     label='Start',
    #     widget=forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
    # )
    # end_date = forms.DateTimeField(
    #     label='End',
    #     widget=forms.widgets.DateTimeInput(attrs={'type':'datetime-local'})
    # )
    class Meta:
        model = Event
        fields = ('name', 'slug', 'location', 'description', 'event_type','start_time', 'end_time', 'rsvp_limit')
                  #'markdown', 'event_type', 'view_permission', 'rsvp_type', 'transportation')

        #this makes formatting easier, but it shows as MM/DD/YYY HH:MM AM/PM which apparently is not valid for the datetimefield :(
        # widgets = {
        #     'start_time': forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
        #     'end_time': forms.widgets.DateTimeInput(attrs={'type':'datetime-local'})
        # }

        help_texts = {
            'start_time': 'Format as dd/mm/yyyy hh:mm (24-hour time! ex. 1pm -> 13:00)',
            'end_time': 'Format as dd/mm/yyyy hh:mm (24-hour time! ex. 1pm -> 13:00)',
        }

        labels = {
            'rsvp_limit': 'RSVP limit',
        }
