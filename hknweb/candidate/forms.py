from django import forms

from .models import OffChallenge
from django.contrib.auth.models import User


class ChallengeRequestForm(forms.ModelForm):

    class Meta:
        model = OffChallenge
        fields = ['name', 'officer', 'description', 'proof']

    officer = forms.ModelChoiceField(queryset=User.objects.filter(groups__name="officer").order_by('username'))
