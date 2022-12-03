from django import forms

from hknweb.events.models import AttendanceResponse


class AttendanceResponseForm(forms.ModelForm):
    required_css_class = "required"
    secret_word = forms.CharField(max_length=255)

    class Meta:
        model = AttendanceResponse
        fields = ("attendance_form", "rsvp", "secret_word", "feedback")

        labels = {
            "feedback": "Submit anonymous feedback on this event",
        }

        widgets = {
            "attendance_form": forms.HiddenInput(),
            "rsvp": forms.HiddenInput(),
        }
