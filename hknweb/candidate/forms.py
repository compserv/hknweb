from django import forms

from .models import OffChallenge
from django.contrib.auth.models import User


class ChallengeRequestForm(forms.ModelForm):

    class Meta:
        model = OffChallenge
        fields = ['name', 'officer', 'description', 'proof']

    # only officers can confirm challenges
    officer = forms.ModelChoiceField(queryset=User.objects \
            .filter(groups__name="officer").order_by('username'))


class ChallengeConfirmationForm(forms.ModelForm):

    class Meta:
        model = OffChallenge
        fields = ['confirmed', 'officer_comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmed'].label = "Check to confirm challenge (if not checked, request will be declined)"
        self.fields['officer_comment'].label = "Optionally add a comment"
