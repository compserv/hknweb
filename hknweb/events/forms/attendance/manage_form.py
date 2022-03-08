from django import forms

from hknweb.events.models import AttendanceForm


class AttendanceFormForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = AttendanceForm
        fields = ("event", "secret_word", "description")

        labels = {
            "secret_word": "Secret word (this is the link to this attendance form)",
        }

        widgets = {
            "event": forms.HiddenInput(),
        }
