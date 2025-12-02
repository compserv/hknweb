from django import forms
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from dal import autocomplete

import csv
import re

from hknweb.candidate.models import BitByteActivity, OffChallenge, ShortLink


TEXT_AREA_STYLE = (
    "resize:none; border: none; border-radius: 0.2em; width: 23.6em; padding: 0.2em;"
)


class ChallengeRequestForm(forms.ModelForm):
    class Meta:
        model = OffChallenge
        fields = ["name", "officer", "proof"]
        widgets = {
            "officer": autocomplete.ModelSelect2(
                url="candidate:autocomplete_officer",
            ),
            "name": forms.Textarea(attrs={"style": TEXT_AREA_STYLE, "rows": 2}),
            "proof": forms.Textarea(attrs={"style": TEXT_AREA_STYLE, "rows": 2}),
        }


class BitByteRequestForm(forms.ModelForm):
    class Meta:
        model = BitByteActivity
        fields = ["participants", "proof"]
        widgets = {
            "participants": autocomplete.ModelSelect2Multiple(
                url="candidate:autocomplete_user"
            ),
            "proof": forms.Textarea(attrs={"style": TEXT_AREA_STYLE, "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super(BitByteRequestForm, self).__init__(*args, **kwargs)
        self.fields["participants"].queryset = User.objects.order_by("username")


class CreateShortLinkForm(forms.ModelForm):
    """
    Form for creating a single shortlink.
    """

    class Meta:
        model = ShortLink
        fields = ["slug", "destination_url", "description"]
        widgets = {
            "slug": forms.TextInput(attrs={"placeholder": "e.g., discord, apply"}),
            "destination_url": forms.URLInput(
                attrs={"placeholder": "https://example.com"}
            ),
            "description": forms.TextInput(
                attrs={"placeholder": "Optional description"}
            ),
        }
        help_texts = {
            "slug": "Short code (letters, numbers, hyphens, underscores only)",
            "destination_url": "Full URL to redirect to",
            "description": "Optional description for reference",
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug and not re.match(r"^[a-zA-Z0-9-_]+$", slug):
            raise ValidationError(
                "Slug can only contain letters, numbers, hyphens, and underscores"
            )
        return slug


class ImportShortLinksForm(forms.Form):
    """
    Form for importing shortlinks from CSV.
    Expected CSV format: "In url,Out url,Creator,..." (additional columns ignored)
    """

    file = forms.FileField(
        help_text='Upload a CSV file with columns: "In url", "Out url", "Creator"'
    )

    REQUIRED_CSV_FIELDNAMES = {"In url", "Out url", "Creator"}
    SLUG_PATTERN = re.compile(r"^[a-zA-Z0-9-_]+$")

    def clean_file(self):
        file_wrapper = self.cleaned_data["file"]

        # Check file extension
        if not file_wrapper.name.endswith(".csv"):
            raise ValidationError("File must be a CSV file")

        return file_wrapper

    def save(self, user):
        """
        Process the CSV and create/update shortlinks.
        Returns tuple: (created_count, updated_count, errors)
        """
        file_wrapper = self.cleaned_data["file"]

        # Decode file and parse CSV
        decoded_file = file_wrapper.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)
        rows = list(reader)

        # Validate fieldnames
        uploaded_fieldnames = set(reader.fieldnames)
        if not self.REQUIRED_CSV_FIELDNAMES.issubset(uploaded_fieldnames):
            missing = self.REQUIRED_CSV_FIELDNAMES.difference(uploaded_fieldnames)
            raise forms.ValidationError(
                f"CSV is missing required columns: {', '.join(missing)}"
            )

        # Process rows
        url_validator = URLValidator()
        created_count = 0
        updated_count = 0
        errors = []

        for i, row in enumerate(rows, start=2):  # Start at 2 (header is row 1)
            slug = row["In url"].strip()
            destination_url = row["Out url"].strip()
            creator_name = row["Creator"].strip()

            # Skip empty rows
            if not slug and not destination_url:
                continue

            # Validate slug
            if not slug:
                errors.append(f"Row {i}: Missing slug")
                continue

            if not self.SLUG_PATTERN.match(slug):
                errors.append(
                    f"Row {i}: Invalid slug '{slug}' (only letters, numbers, hyphens, underscores allowed)"
                )
                continue

            # Validate destination URL
            if not destination_url:
                errors.append(f"Row {i}: Missing destination URL for slug '{slug}'")
                continue

            try:
                url_validator(destination_url)
            except ValidationError:
                errors.append(f"Row {i}: Invalid URL '{destination_url}' for slug '{slug}'")
                continue

            # Create or update shortlink
            try:
                shortlink, created = ShortLink.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "destination_url": destination_url,
                        "description": f"Created by {creator_name}",
                        "created_by": user,
                        "active": True,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            except Exception as e:
                errors.append(f"Row {i}: Error processing slug '{slug}': {str(e)}")

        return created_count, updated_count, errors
