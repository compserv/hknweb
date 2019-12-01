from django import forms

from django.conf import settings
from .models import DepTour
from django.contrib.auth.models import User


class TourRequest(forms.ModelForm):

    class Meta:
        model = DepTour
        fields = ['name', 'desired_date', 'email', 'confirm_email', 'phone', 'comments']
        help_texts = {
            'desired_date': 'mm/dd/yyyy hh:mm, 24-hour time',
            # 'end_time': 'mm/dd/yyyy hh:mm, 24-hour time',
        }

class TourConfirmationForm(forms.ModelForm):

    class Meta:
        model = DepTour
        fields = ['confirmed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmed'].label = "Check to confirm tour request (if not checked, request will be declined)"
        # self.fields['officer_comment'].label = "Optionally add a comment"
