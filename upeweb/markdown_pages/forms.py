from django import forms
from markdownx.fields import MarkdownxFormField

class EditPageForm(forms.Form):
    name        = forms.CharField(max_length=255)
    path        = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    body        = MarkdownxFormField()
