from django import forms
from .models import Slot, Course, Tutor


class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ('hour', 'day', 'room', 'tutors')

    tutors = forms.ModelMultipleChoiceField(queryset=Tutor.objects.order_by('name'))

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('name',)

class TutorForm(forms.ModelForm):

    class Meta:
        model = Tutor
        fields = ('name', 'courses')

    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.order_by('name'))