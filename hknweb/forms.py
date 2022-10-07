from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    SetPasswordForm,
)
from django.conf import settings
from django.contrib.auth.models import Group

import csv

import string

import secrets

from hknweb.models import User, Profile
from hknweb.coursesemester.models import Semester


class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password")


class ProfileForm(forms.ModelForm):
    required_css_class = "required"

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"autocomplete": "off"}), required=False
    )
    graduation_date = forms.DateField(
        widget=forms.DateInput(attrs={"autocomplete": "off"}), required=False
    )

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


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("picture",)


class SemesterSelectForm(forms.Form):
    semester = forms.ModelChoiceField(Semester.objects.order_by("-year", "semester"))


class ProvisionCandidatesForm(forms.Form):
    file = forms.FileField()
    REQUIRED_CSV_FIELDNAMES = set(["First name", "Last name", "Berkeley email"])
    REQUIRED_EMAIL_SUFFIX = "@berkeley.edu"

    CREATE_ACCOUNT_ERROR_MESSAGES = {
        "invalid email": 'Emails must end with "@berkeley.edu". The following emails are invalid: ',
    }
    PASSWORD_LENGTH = 20

    def save(self):
        # Retrieve relevant objects
        required_csv_fieldnames = self.REQUIRED_CSV_FIELDNAMES
        required_email_suffix = self.REQUIRED_EMAIL_SUFFIX
        password_length = self.PASSWORD_LENGTH
        file_wrapper = self.cleaned_data["file"]

        # Decode file from cleaned_data and throw it into a csv
        decoded_file = file_wrapper.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)
        rows = list(reader)

        # Check that we have the proper fieldnames
        uploaded_fieldnames = set(reader.fieldnames)
        if uploaded_fieldnames != required_csv_fieldnames:
            difference = required_csv_fieldnames.difference(uploaded_fieldnames)
            raise forms.ValidationError(f"Input csv is missing the following columns: {difference}")

        def email_to_username(email: str) -> str:
            username = None
            if email.endswith(required_email_suffix):
                username = email[:-len(required_email_suffix)]

            return username

        # Get existing usernames
        usernames = []
        invalid_emails = []
        for row in rows:
            email = row["Berkeley email"]
            username = email_to_username(email)

            if username:
                usernames.append(username)
            else:
                invalid_emails.append(email)

            row["username"] = username

        existing_usernames = set(User.objects.filter(username__in=usernames).values_list("username", flat=True))

        # Setup account provisioning
        group = Group.objects.get(name=settings.CAND_GROUP)

        alphabet = string.ascii_letters + string.digits
        def generate_password() -> str:
            password = "".join(secrets.choice(alphabet) for _ in range(password_length))

            return password

        for row in rows:
            # If username is None or already exists, skip provisioning
            if (row["username"] is None) or (row["username"] in existing_usernames):
                continue

            # Generate a password
            password = generate_password()

            # Construct user object
            user = User.objects.create_user(
                username=row["username"],
                first_name=row["First name"],
                last_name=row["Last name"],
                email=row["Berkeley email"],
                password=password,
            )
            user.save()

            # Add user to the candidates group
            group.user_set.add(user)

            # Email user with account activitation information
            # !TODO
            # user.email_user

        # For any accounts not created because of invalid email, report to the user
        # !TODO
