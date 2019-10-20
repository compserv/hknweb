from django import forms

from django.conf import settings
from .models import OffChallenge
from django.contrib.auth.models import User


class ChallengeRequestForm(forms.ModelForm):

    class Meta:
        model = OffChallenge
        fields = ['name', 'officer', 'description', 'proof']

    # only officers can confirm challenges
    officer = forms.ModelChoiceField(queryset=User.objects
            .filter(groups__name=settings.OFFICER_GROUP).order_by('username'))

    officer.label_from_instance = lambda obj: \
            "{} ({} {})".format(obj.username, obj.first_name, obj.last_name)


class ChallengeConfirmationForm(forms.ModelForm):

    class Meta:
        model = OffChallenge
        fields = ['officer_confirmed', 'officer_comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['officer_confirmed'].label = "Choose \"Yes\" to confirm challenge, \"No\" to decline"
        self.fields['officer_comment'].label = "Optionally add a comment"
