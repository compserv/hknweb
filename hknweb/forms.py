from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    SetPasswordForm,
)

from hknweb.models import User, Profile


class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password")


class ProfileForm(forms.ModelForm):
    required_css_class = "required"

    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"autocomplete": "off"}), required=False)
    graduation_date = forms.DateField(widget=forms.DateInput(attrs={"autocomplete": "off"}), required=False)

    class Meta:
        model = Profile
        fields = (
            "private",
            "phone_number",
            "date_of_birth",
            "resume",
            "graduation_date",
            "candidate_semester",
        )


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=200, required=True)
    candidate_password = forms.CharField(max_length=30, required=False)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (email is None) or not email.endswith(
            "berkeley.edu"
        ):  # lgtm [py/incomplete-url-substring-sanitization]
            raise forms.ValidationError(
                "Please a berkeley.edu email to register!", code="invalid"
            )
        else:
            return email

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )


class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=30, label="New password", widget=forms.PasswordInput
    )
    new_password1.help_text = ""


class ValidPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("password",)
