from django import forms
from hknweb.models import User
from hknweb.models import Profile
from .models import ReviewSession


class ReviewSessionForm(forms.ModelForm):

    # start_date = forms.DateTimeField(
    #     label='Start',
    #     widget=forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
    # )
    # end_date = forms.DateTimeField(
    #     label='End',
    #     widget=forms.widgets.DateTimeInput(attrs={'type':'datetime-local'})
    # )
    class Meta:
        model = ReviewSession
        fields = ('name', 'slug', 'location', 'description', 'start_time', 'end_time')
                  #'markdown', 'event_type', 'view_permission', 'rsvp_type', 'transportation')

        #this makes formatting easier, but it shows as MM/DD/YYY HH:MM AM/PM which apparently is not valid for the datetimefield :(
        # widgets = {
            # 'start_time': forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
        #     # 'end_time': forms.widgets.DateTimeInput(attrs={'type':'datetime-local'})
        # }
        # field_classes = {
        #     'start_time': forms.widgets.DateTimeInput,
        #     'end_time': forms.widgets.DateTimeInput,
        # }
        help_texts = {
            'start_time': 'mm/dd/yyyy hh:mm, 24-hour time',
            'end_time': 'mm/dd/yyyy hh:mm, 24-hour time',
            'slug': 'e.g. <semester>-<name>',
        }

        labels = {
            'slug': 'URL-friendly name',
        }
