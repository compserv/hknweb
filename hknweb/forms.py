from django import forms
from hknweb.models import User
from hknweb.models import Profile

class SettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image', 'private', 'phone_number', 'date_of_birth', 'resume', 'graduation_date')