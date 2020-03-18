from django import forms
from django.conf import settings
from .models import DepTour
from django.forms.widgets import SelectDateWidget
import datetime


class TourRequest(forms.ModelForm):
    date = forms.DateField(widget=SelectDateWidget(), label='Desired Date', initial=datetime.date.today)
    desired_time = forms.TimeField(help_text='hh:mm 24-hour time', label='Desired Time')
    class Meta:
        model = DepTour
        fields = ['name', 'date', 'desired_time', 'email', 'confirm_email', 'phone', 'comments']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date
    
    def clean(self):
        cleaned_data = super(TourRequest, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if email and confirm_email:
            if email != confirm_email:
                raise forms.ValidationError("Emails do not match.")
        return cleaned_data
