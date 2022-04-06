from django import forms
from django.utils import timezone

from hknweb.studentservices.models import DepTour, Resume
from hknweb.utils import DATETIME_12_HOUR_FORMAT
from hknweb.events.utils import DATETIME_WIDGET_NO_AUTOCOMPLETE


class DocumentForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Resume
        fields = ("name", "document", "notes", "email")

        labels = {
            "document": "Resume (please submit a PDF)",
            "notes": "What type of feedback/help are you looking for? What types of companies/schools etc are you applying for and what fields are you interested in?",
        }


class TourRequest(forms.ModelForm):
    datetime = forms.DateTimeField(
        input_formats=(DATETIME_12_HOUR_FORMAT,),
        widget=DATETIME_WIDGET_NO_AUTOCOMPLETE,
        label="Desired Date and Time",
    )

    class Meta:
        model = DepTour
        fields = ["name", "datetime", "email", "phone", "comments"]

    def clean(self):
        super().clean()
        datetime = self.cleaned_data.get("datetime")
        if datetime and datetime < timezone.now():
            self.add_error("datetime", "Desired date and time is in the past")

        return self.cleaned_data
