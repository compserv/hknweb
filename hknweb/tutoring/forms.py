from django import forms
from .models import TimeSlot, Slot, Course, Tutor, TimeSlotPreference, CoursePreference
from django_range_slider.fields import RangeSliderField

class TimeSlotForm(forms.ModelForm):
    class Met:
        model = TimeSlot
        fields=('hour', 'day')

class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ('timeslot', 'room', 'tutors')

    tutors = forms.ModelMultipleChoiceField(queryset=Tutor.objects.order_by('name'))

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('name',)

class TutorForm(forms.ModelForm):

    class Meta:
        model = Tutor
        fields = ('name',)

    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.order_by('name'))

class TimeSlotPreferenceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.tutor = kwargs.pop('tutor')
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        timeslots = TimeSlot.objects.all().order_by('timeslot_id')
        for timeslot in timeslots:
            pref = TimeSlotPreference.objects.get(tutor=self.tutor, timeslot=timeslot)
            field_name = 'timeslot_time_preference_%s' % (timeslot.timeslot_id,)
            self.fields[field_name] = forms.IntegerField(label="", widget=forms.RadioSelect())
            self.fields[field_name].initial = pref.time_preference
            field_name = 'timeslot_office_preference_%s' % (timeslot.timeslot_id,)
            self.fields[field_name] = RangeSliderField(minimum=0, maximum=4)
            self.fields[field_name].initial = pref.office_preference
    #Returns data in form: [[Slotpreference, time_preference, office_preference] ... ]
    def save_slot_preference_data(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('timeslot_time_preference_'):
                timeslot_id = int(name.replace('timeslot_time_preference_', ''))
                timeslot = TimeSlot.objects.get(timeslot_id=timeslot_id)
                pref = TimeSlotPreference.objects.filter(timeslot=timeslot, tutor=self.tutor)
                pref.time_preference = value
                pref.save()
            elif name.startsiwht('timeslot_office_preference_'):
                timeslot_id = int(name.replace('timeslot_office_preference_', ''))
                timeslot = TimeSlot.objects.get(timeslot_id=timeslot_id)
                pref = TimeSlotPreference.objects.filter(timeslot=timeslot, tutor=self.tutor)
                pref.time_preference = value
                pref.save()


