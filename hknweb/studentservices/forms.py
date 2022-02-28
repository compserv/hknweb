from django import forms
from hknweb.studentservices.models import Resume


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ("name", "document", "notes", "email")
