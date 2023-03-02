from django import forms

from hknweb.utils import DATETIME_12_HOUR_FORMAT
from hknweb.events.models import Event
from hknweb.events.utils import DATETIME_WIDGET_NO_AUTOCOMPLETE


class EventForm(forms.ModelForm):
    required_css_class = "required"
    start_time = forms.DateTimeField(
        input_formats=(DATETIME_12_HOUR_FORMAT,), widget=DATETIME_WIDGET_NO_AUTOCOMPLETE
    )
    end_time = forms.DateTimeField(
        input_formats=(DATETIME_12_HOUR_FORMAT,), widget=DATETIME_WIDGET_NO_AUTOCOMPLETE
    )
    repeat_num_times = forms.IntegerField(
        min_value=0,
        required=False,
        label="Number of Repeats (after first occurrence)",
        initial=0,
    )
    repeat_period = forms.IntegerField(
        min_value=0,
        required=False,
        label="How often this event repeats (in weeks)",
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
            "photographer",
        )

        labels = {
            "rsvp_limit": "RSVP limit",
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if (start_time is None) or (end_time is None):
            error_source = "start_time" if (start_time is None) else "end_time"
            self.add_error(error_source, "Please use the time picker to select the time, the formatter is picky")
        elif end_time < start_time:
            self.add_error("end_time", "End Time is not after Start Time")
