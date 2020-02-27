from django import forms
from django.conf import settings
from .models import DepTour
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget
# from django.contrib.admin.widgets import AdminDateWidget

import datetime


class TourRequest(forms.ModelForm):
    date = forms.DateField(widget=SelectDateWidget(), label='Desired Date')
    desired_time = forms.TimeField(help_text='hh:mm 24-hour time', label='Desired Time')
    class Meta:
        model = DepTour
        fields = ['name', 'date', 'desired_time', 'email', 'phone', 'comments']

    # def clean_verify_email(self):
    #     second_email = self.cleaned_data['verify_email']
    #     first_email = self.cleaned_data['email']
    #     if second_email != first_email:
    #         raise forms.ValidationError(('Invalid email: "%(second)s" does not match "%(first)s"'), code='emails_not_matching', params={'first': first_email, 'second': second_email})