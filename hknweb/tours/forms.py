from django import forms

from django.conf import settings
from .models import DepTour
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import SelectDateWidget

from django.forms.widgets import SplitDateTimeWidget

from datetime import datetime


class TourRequest(forms.ModelForm):
    desired_date = forms.DateField(widget=SelectDateWidget())
    desired_time = forms.TimeField(help_text='hh:mm 24-hour time')
    # desired_date = forms.DateField(widget=AdminDateWidget())
    class Meta:
        # desired_date = DateField(widget=AdminDateWidget)
        model = DepTour
        fields = ['name', 'desired_date', 'desired_time', 'email', 'phone', 'comments']
        help_texts = {
            'desired_date': 'mm/dd/yyyy hh:mm, 24-hour time',
            'desired_time': 'hh:mm 24-hour time',
        }

    def clean_verify_email(self):
        second_email = self.cleaned_data['verify_email']
        first_email = self.cleaned_data['email']
        if second_email != first_email:
            raise forms.ValidationError(('Invalid email: "%(second)s" does not match "%(first)s"'), code='emails_not_matching', params={'first': first_email, 'second': second_email})

# class TourConfirmationForm(forms.ModelForm):
#
#     class Meta:
#         model = DepTour
#         fields = ['confirmed']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['confirmed'].label = "Check to confirm tour request (if not checked, request will be declined)"
