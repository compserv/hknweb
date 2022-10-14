from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    SetPasswordForm,
)
from django.conf import settings
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail
from django.contrib import messages
from django.urls import reverse
from django.core.mail import get_connection, EmailMultiAlternatives

import csv

import string

import secrets

from hknweb.models import User, Profile
from hknweb.coursesemester.models import Semester
from hknweb.utils import get_rand_photo
from hknweb.utils import get_rand_photo


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

    def send_candidate_account_emails(self, request) -> None:
        # Retreive relevant objects from self
        email_information = self.email_information

        # Convenience method for emailing users
        email_subject = "Welcome to HKN - dev-hkn candidate account information"
        email_links = {
            "settings_link": "account-settings",
            "events_index_link": "events:index",
            "candidate_portal_link": "candidate:candidate_portal",
        }
        email_links = {
            k: request.build_absolute_uri(reverse(v)) for k, v in email_links.items()
        }

        def create_email(user: User, password: str, connection):
            email_message = render_to_string(
                "account/new_candidate_account_email.html",
                {
                    "subject": email_subject,
                    "first_name": user.first_name,
                    "username": user.username,
                    "password": password,
                    "img_link": get_rand_photo(),
                    **email_links,
                },
            )

            msg = EmailMultiAlternatives(
                email_subject, email_subject, settings.NO_REPLY_EMAIL, [user.email], connection=connection
            )
            msg.attach_alternative(email_message, "text/html")

            return msg

        # Send emails using the same connection
        with get_connection() as connection:
            email_messages = [create_email(*info, connection) for info in email_information]

            for email in email_messages:
                email.send()

    def add_messages(self, request) -> None:
        # For any accounts not created because of invalid email, report to the user

        # Retrieve relevant objects from self
        invalid_emails = self.invalid_emails

        if invalid_emails:
            messages.error(
                request,
                f"All accounts created successfully except the following with invalid emails: {invalid_emails}. As a reminder, all emails must end in '@berkeley.edu'.",
            )
        else:
            messages.info(request, "All accounts successfully created!")

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
            raise forms.ValidationError(
                f"Input csv is missing the following columns: {difference}"
            )

        def email_to_username(email: str) -> str:
            username = None
            if email.endswith(required_email_suffix):
                username = email[: -len(required_email_suffix)]

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

        existing_usernames = set(
            User.objects.filter(username__in=usernames).values_list(
                "username", flat=True
            )
        )

        # Setup account provisioning utils
        # Get candidate group to add users to
        group = Group.objects.get(name=settings.CAND_GROUP)

        # Convenience function for generating a password
        alphabet = string.ascii_letters + string.digits

        def generate_password() -> str:
            password = "".join(secrets.choice(alphabet) for _ in range(password_length))

            return password

        email_information = []
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

            # Add information for sending emails
            email_information.append((user, password))

        self.email_information = email_information

        # Save information for adding messages
        self.invalid_emails = invalid_emails
