import urllib
import json

from django import forms
from hknweb.models import User
from hknweb.models import Profile
from hknweb.alumni.models import Alumnus
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.conf import settings

class SettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('picture', 'private', 'phone_number', 'date_of_birth', 'resume', 'graduation_date')

class SignupForm(UserCreationForm):
     first_name = forms.CharField(max_length=30, required=True)
     last_name = forms.CharField(max_length=30, required=True)
     email = forms.EmailField(max_length=200, required=True)

     def clean_email(self):
         email = self.cleaned_data.get('email')
         if (email == None or email.split('@')[-1] != 'berkeley.edu'
         or email.split('@')[1] != email.split('@')[-1]):
             raise forms.ValidationError('Please use your Berkeley email', code='invalid')
         else:
             return email

     def clean(self):
         super().clean()
         # reCAPTCHA validation
         recaptcha_response = self.cleaned_data.get('g-recaptcha-response')
         url = 'https://www.google.com/recaptcha/api/siteverify'
         values = {
             'secret': settings.RECAPTCHA_PRIVATE_KEY,
             'response': recaptcha_response
         }
         data = urllib.parse.urlencode(values).encode()
         req =  urllib.request.Request(url, data=data)
         response = urllib.request.urlopen(req)
         result = json.loads(response.read().decode())
         if result['success']:
             return recaptcha_response
         else:
             raise forms.ValidationError('Invalid reCAPTCHA. Please try again.', code='invalid')

     class Meta:
          model = User
          fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class UpdatePasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(max_length=30, required=True, label = "New password")
    new_password1.help_text = ''

class ValidPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password',)
