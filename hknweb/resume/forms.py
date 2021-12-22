from django import forms
from hknweb.resume.models import Resume


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ("name", "document", "notes", "email")
