from django import forms

from hknweb.utils import DATETIME_12_HOUR_FORMAT
from hknweb.events.models import Event, AttendanceForm
from hknweb.events.utils import DATETIME_WIDGET_NO_AUTOCOMPLETE


class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=(DATETIME_12_HOUR_FORMAT,), widget=DATETIME_WIDGET_NO_AUTOCOMPLETE
    )
    end_time = forms.DateTimeField(
        input_formats=(DATETIME_12_HOUR_FORMAT,), widget=DATETIME_WIDGET_NO_AUTOCOMPLETE
    )
    recurring_num_times = forms.IntegerField(
        min_value=0, required=False, label="Number of occurences", initial=0
    )
    recurring_period = forms.IntegerField(
        min_value=0,
        required=False,
        label="How often this event re-occurs (in weeks)",
        initial=0,
    )

    class Meta:
        model = Event
        fields = (
            "name",
            "location",
            "description",
            "event_type",
            "start_time",
            "end_time",
            "rsvp_limit",
            "access_level",
        )

        labels = {
            "rsvp_limit": "RSVP limit",
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if end_time < start_time:
            self.add_error("end_time", "End Time is not after Start Time")


class EventUpdateForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=(DATETIME_12_HOUR_FORMAT,))
    end_time = forms.DateTimeField(input_formats=(DATETIME_12_HOUR_FORMAT,))

    class Meta:
        model = Event
        fields = [
            "name",
            "start_time",
            "end_time",
            "location",
            "event_type",
            "description",
            "rsvp_limit",
            "access_level",
        ]

        labels = {
            "rsvp_limit": "RSVP limit",
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if end_time < start_time:
            self.add_error("end_time", "End Time is not after Start Time")


class AttendanceFormForm(forms.ModelForm):
    class Meta:
        model = AttendanceForm
        fields = ("event", "secret_word")

        labels = {
            "secret_word": "Secret word (this is the link to this attendance form)",
        }
