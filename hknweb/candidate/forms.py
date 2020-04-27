from django import forms
from .models import OffChallenge, BitByteActivity
from django.contrib.auth.models import User

from dal import autocomplete

class ChallengeRequestForm(forms.ModelForm):

    class Meta:
        model = OffChallenge
        fields = ['name', 'officer', 'description', 'proof']
        widgets = {
            'officer': autocomplete.ModelSelect2(url='candreq/autocomplete')
        }


class ChallengeConfirmationForm(forms.ModelForm):

    class Meta:
        model = OffChallenge
        fields = ['officer_confirmed', 'officer_comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['officer_confirmed'].label = "Choose \"Yes\" to confirm challenge, \"No\" to decline" \
                                                 " (after you confirm, csec still has to confirm as well)"
        self.fields['officer_comment'].label = "Optionally add a comment"


class BitByteRequestForm(forms.ModelForm):

    class Meta:
        model = BitByteActivity
        fields = ['participants', 'proof']
        widgets = {
            'participants': autocomplete.ModelSelect2Multiple(url='bitbyte/autocomplete')
        }

    def __init__(self, *args, **kwargs):
        super(BitByteRequestForm, self).__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.order_by('username')
