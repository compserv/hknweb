import datetime

from django import forms

from hknweb.studentservices.models import DepTour, Resume, ReviewSession


class DocumentForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Resume
        fields = ("name", "document", "notes", "email")

        labels = {
            "document": "Resume (please submit a PDF)",
            "notes": "What type of feedback/help are you looking for? What types of companies/schools etc are you applying for and what fields are you interested in?",
        }


class ReviewSessionForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=("%m/%d/%Y %I:%M %p",))
    end_time = forms.DateTimeField(input_formats=("%m/%d/%Y %I:%M %p",))

    class Meta:
        model = ReviewSession
        fields = ("name", "slug", "location", "description", "start_time", "end_time")

        help_texts = {
            "start_time": "mm/dd/yyyy hh:mm, 24-hour time",
            "end_time": "mm/dd/yyyy hh:mm, 24-hour time",
            "slug": "e.g. <semester>-<name>",
        }

        widgets = {
            "slug": forms.TextInput(attrs={"placeholder": "e.g. <semester>-<name>"}),
        }

        labels = {
            "slug": "URL-friendly name",
        }


class ReviewSessionUpdateForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=("%m/%d/%Y %I:%M %p",))
    end_time = forms.DateTimeField(input_formats=("%m/%d/%Y %I:%M %p",))

    class Meta:
        model = ReviewSession
        fields = ["name", "slug", "start_time", "end_time", "location", "description"]

        labels = {
            "slug": "URL-friendly name",
        }


class TourRequest(forms.ModelForm):
    datetime = forms.DateTimeField(
        help_text="MM/DD/YYYY hh:mm AM/PM",
        input_formats=("%m/%d/%Y %I:%M %p",),
        label="Desired Date and Time",
    )
    confirm_email = forms.EmailField(max_length=100)

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
