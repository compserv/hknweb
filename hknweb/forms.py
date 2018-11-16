from django import forms

from .models import Profile
from .models import User


class SettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image', 'private', 'phone_number', 'date_of_birth', 'resume', 'graduation_date')
