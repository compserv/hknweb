from django import forms

from hknweb.events.models import EventPhoto


class EventPhotoForm(forms.ModelForm):
    class Meta:
        model = EventPhoto
        fields = ("photo", "event")
