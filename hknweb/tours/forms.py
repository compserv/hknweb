from django import forms
from .models import DepTour
from django.forms.widgets import SelectDateWidget
import datetime

MAX_STRLEN = 85


class TourRequest(forms.ModelForm):
    datetime = forms.DateTimeField(
        help_text="MM/DD/YYYY hh:mm AM/PM",
        input_formats=("%m/%d/%Y %I:%M %p",),
        label="Desired Date and Time",
    )
    confirm_email = forms.EmailField(max_length=MAX_STRLEN)

    class Meta:
        model = DepTour
        fields = ["name", "datetime", "email", "confirm_email", "phone", "comments"]

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date

    def clean_desired_time(self):
        date = self.cleaned_data.get("date", 0)
        time = self.cleaned_data["desired_time"]
        if date == datetime.date.today() and time < datetime.datetime.now().time():
            raise forms.ValidationError("Time cannot be in the past!")
        return time

    def clean_confirm_email(self):
        email = self.cleaned_data["email"]
        confirm_email = self.cleaned_data["confirm_email"]
        if email and confirm_email:
            if email != confirm_email:
                raise forms.ValidationError("Emails do not match.")
        return confirm_email
