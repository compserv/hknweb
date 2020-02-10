from django import forms

from django.conf import settings
from .models import DepTour
from django.contrib.auth.models import User


class TourRequest(forms.ModelForm):
    confirm_email = forms.EmailField(label="Confirm Email")
    class Meta:
        model = DepTour
        fields = ['name', 'desired_date', 'email', 'confirm_email', 'phone', 'comments']
        help_texts = {
            'desired_date': 'mm/dd/yyyy hh:mm, 24-hour time',
            # 'end_time': 'mm/dd/yyyy hh:mm, 24-hour time',
        }

    def clean_verify_email(self):
        second_email = self.cleaned_data['verify_email']
        first_email = self.cleaned_data['email']
        if second_email != first_email:
            raise forms.ValidationError(_('Invalid email: "%(second)s" does not match "%(first)s"'), code='emails_not_matching', params={'first': first_email, 'second': second_email})

class TourConfirmationForm(forms.ModelForm):

    class Meta:
        model = DepTour
        fields = ['confirmed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmed'].label = "Check to confirm tour request (if not checked, request will be declined)"
