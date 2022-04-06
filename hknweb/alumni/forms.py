from django import forms
from .models import Alumnus


class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumnus
        fields = (
            "first_name",
            "last_name",
            "perm_email",
            "mailing_list",
            "grad_season",
            "grad_year",
            "grad_school",
            "company",
            "job_title",
            "salary",
            "city",
            "country_state",
            "suggestions",
        )
