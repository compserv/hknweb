from django import forms
from .models import CoursePreference, Room, TimeSlot, \
    TutorCourse, TimeSlotPreference

COURSE_PREFERENCE_CHOICES = [
    (-1, 'Have not yet taken course'),
    (0, 'Currently taken course'),
    (1, 'Completed course'),
    (2, 'Complete and prefer tutoring for course')
]
class CoursePreferenceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.tutor = kwargs.pop('tutor')
        super().__init__(*args, **kwargs)
        courses = TutorCourse.objects.all().order_by('id')
        for course in courses:
            pref = CoursePreference.objects.get(tutor=self.tutor, course=course)
            field_name = 'course_preference_%s' % (course.id,)
            self.fields[field_name] = forms.IntegerField(label=str(course.course), widget=forms.RadioSelect(choices=COURSE_PREFERENCE_CHOICES))
            self.fields[field_name].initial = pref.preference
    def save_course_preference_data(self):
        for name, value in self.cleaned_data.items():
            id = int(name.replace('course_preference_', ''))
            course = TutorCourse.objects.get(id=id)
            pref = CoursePreference.objects.get(course=course, tutor=self.tutor)
            pref.preference = value
            pref.save()

SLOT_PREFERENCE_CHOICES= [
        (0, 'Unavailable'),
        (1, 'Available'),
        (2, 'Preferred'),
    ]
ADJACENT_PREFERENCE_CHOIES = [
    (-1, 'No'),
    (0, "Don't care"),
    (1, 'Yes')
]
class TimeSlotPreferenceForm(forms.Form):
    adjacent_pref = forms.IntegerField(widget=forms.RadioSelect(choices=ADJACENT_PREFERENCE_CHOIES))
    num_assignments = forms.IntegerField()
    tutor_name = forms.CharField()
    def __init__(self, *args, **kwargs):
        self.tutor = kwargs.pop('tutor')
        super().__init__(*args, **kwargs)
        self.fields['tutor_name'].initial = self.tutor.name
        self.fields['adjacent_pref'].initial = self.tutor.adjacent_pref
        self.fields['num_assignments'].initial = self.tutor.num_assignments
        timeslots = TimeSlot.objects.all().order_by('timeslot_id')
        for timeslot in timeslots:
            pref = TimeSlotPreference.objects.get(tutor=self.tutor, timeslot=timeslot)
            field_name = 'timeslot_time_preference_%s' % (timeslot.timeslot_id,)
            self.fields[field_name] = forms.IntegerField(widget=forms.RadioSelect(choices=SLOT_PREFERENCE_CHOICES))
            self.fields[field_name].initial = pref.time_preference

            number_of_tutor_rooms = Room.objects.all().count()

            if number_of_tutor_rooms == 1:
                # Doesn't matter preference, there's only one room anyway
                pass
            elif number_of_tutor_rooms == 2:
                field_name = 'timeslot_office_preference_%s' % (timeslot.timeslot_id,)
                self.fields[field_name] = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'min':-2, 'max': 2, 'step': 1}))
                self.fields[field_name].initial = pref.office_preference
            else:
                # TODO: In the event there is multiple rooms (low priority)
                pass
        
    def save_slot_preference_data(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('timeslot_time_preference_'):
                timeslot_id = int(name.replace('timeslot_time_preference_', ''))
                timeslot = TimeSlot.objects.get(timeslot_id=timeslot_id)
                pref = TimeSlotPreference.objects.get(timeslot=timeslot, tutor=self.tutor)
                pref.time_preference = value
                pref.save(update_fields=["time_preference"])
            elif name.startswith('timeslot_office_preference_'):
                timeslot_id = int(name.replace('timeslot_office_preference_', ''))
                timeslot = TimeSlot.objects.get(timeslot_id=timeslot_id)
                pref = TimeSlotPreference.objects.get(timeslot=timeslot, tutor=self.tutor)
                pref.office_preference = value
                pref.save(update_fields=["office_preference"])
            elif name == "adjacent_pref":
                self.tutor.adjacent_pref = value
            elif name == "num_assignments":
                self.tutor.num_assignments = value
            elif name == "tutor_name":
                self.tutor.name = value
        self.tutor.save(update_fields=["adjacent_pref", "num_assignments", "name"])

class TutoringAlgorithmOutputForm(forms.Form):
    output = forms.FileField(label="Upload tutoring algorithm output file")

