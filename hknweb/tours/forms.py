from django import forms

from django.conf import settings
from .models import OffChallenge
from django.contrib.auth.models import User


class TourRequest(forms.ModelForm):

    class Meta:
        model = DepTour
        fields = ['name', 'desired_date', 'email', 'confirm_email', 'phone', 'comments']


class TourConfirmationForm(forms.ModelForm):

    class Meta:
        model = DepTour
        fields = ['confirmed', 'officer_comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmed'].label = "Check to confirm challenge (if not checked, request will be declined)"
        self.fields['officer_comment'].label = "Optionally add a comment"
