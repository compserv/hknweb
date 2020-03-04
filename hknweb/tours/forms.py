from django import forms
from .models import DepTour
from django.forms.widgets import SelectDateWidget

class TourRequest(forms.ModelForm):
    date = forms.DateField(widget=SelectDateWidget(), label='Desired Date')
    desired_time = forms.TimeField(help_text='hh:mm 24-hour time', label='Desired Time')
    class Meta:
        model = DepTour
        fields = ['name', 'date', 'desired_time', 'email', 'phone', 'comments']