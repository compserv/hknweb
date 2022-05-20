from django import forms

from hknweb.utils import DATETIME_12_HOUR_FORMAT
from hknweb.events.models import Event


class EventUpdateForm(forms.ModelForm):
    required_css_class = "required"
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
            "photographer",
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
