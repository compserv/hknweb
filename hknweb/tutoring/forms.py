from django import forms
from .models import (
    CoursePreference,
    RoomPreference,
    Slot,
    TimeSlot,
    TutorCourse,
    TimeSlotPreference,
)

COURSE_PREFERENCE_CHOICES = [
    (-1, "Have not yet taken course"),
    (0, "Currently taken course"),
    (1, "Completed course"),
    (2, "Complete and prefer tutoring for course"),
]


class CoursePreferenceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.tutor = kwargs.pop("tutor")
        super().__init__(*args, **kwargs)
        courses = TutorCourse.objects.all().order_by("id")
        for course in courses:
            pref = CoursePreference.objects.get(tutor=self.tutor, course=course)
            field_name = "course_preference_%s" % (course.id,)
            self.fields[field_name] = forms.IntegerField(
                label=str(course.course),
                widget=forms.RadioSelect(choices=COURSE_PREFERENCE_CHOICES),
            )
            self.fields[field_name].initial = pref.preference

    def save_course_preference_data(self):
        for name, value in self.cleaned_data.items():
            id = int(name.replace("course_preference_", ""))
            course = TutorCourse.objects.get(id=id)
            pref = CoursePreference.objects.get(course=course, tutor=self.tutor)
            pref.preference = value
            pref.save()


SLOT_PREFERENCE_CHOICES = [
    (0, "Unavailable"),
    (1, "Available"),
    (2, "Preferred"),
]
ADJACENT_PREFERENCE_CHOIES = [(-1, "No"), (0, "Don't care"), (1, "Yes")]


class TimeSlotPreferenceForm(forms.Form):
    adjacent_pref = forms.IntegerField(
        widget=forms.RadioSelect(choices=ADJACENT_PREFERENCE_CHOIES)
    )
    num_assignments = forms.IntegerField()
    tutor_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.tutor = kwargs.pop("tutor")
        super().__init__(*args, **kwargs)
        self.fields["tutor_name"].initial = self.tutor.name
        self.fields["adjacent_pref"].initial = self.tutor.adjacent_pref
        self.fields["num_assignments"].initial = self.tutor.num_assignments
        timeslots = TimeSlot.objects.all().order_by("timeslot_id")

        ROOM_PREFERENCE_CHOICES_BASE = [(0, "No Preference")]
        # ROOM_PREFERENCE_CHOICES += [
        #     (room.id + 1, str(room))
        #     for room in Room.objects.all()
        # ]

        for timeslot in timeslots:
            timeslot_pref = TimeSlotPreference.objects.get(
                tutor=self.tutor, timeslot=timeslot
            )
            field_name = "timeslot_time_preference_%s" % (timeslot.timeslot_id,)
            self.fields[field_name] = forms.IntegerField(
                widget=forms.RadioSelect(choices=SLOT_PREFERENCE_CHOICES)
            )
            self.fields[field_name].initial = timeslot_pref.preference
            self.fields[field_name].label = "Timeslot Availability"

            room_prefs = RoomPreference.objects.filter(
                tutor=self.tutor, timeslot=timeslot
            )

            rooms_slot_available = Slot.objects.filter(timeslot=timeslot).order_by(
                "room__id"
            )
            number_of_tutor_rooms = rooms_slot_available.count()

            field_name = "timeslot_office_preference_%s" % (timeslot.timeslot_id,)

            if number_of_tutor_rooms == 1:
                one_room_pref = room_prefs.get(room=rooms_slot_available.first().room)
                self.fields[field_name] = forms.IntegerField(
                    widget=forms.RadioSelect(
                        choices=[(one_room_pref.room.id + 1, str(one_room_pref.room))]
                    )
                )
                self.fields[field_name].label = "Room Preference"
                self.fields[field_name].initial = one_room_pref.room.id + 1
            else:
                self.fields[field_name] = forms.IntegerField(
                    widget=forms.RadioSelect(
                        choices=ROOM_PREFERENCE_CHOICES_BASE
                        + [
                            (room_slot.room.id + 1, str(room_slot.room))
                            for room_slot in rooms_slot_available
                        ]
                    )
                )
                chosen = 0
                highest = 0
                for room_slot in rooms_slot_available:
                    one_room_pref = room_prefs.get(room=room_slot.room)
                    # 0 means don't care, so no == 0
                    if (
                        one_room_pref.preference > 0
                        and one_room_pref.preference > highest
                    ):
                        chosen = (
                            one_room_pref.room.id + 1
                        )  # Shift forward by one for No Preference
                        highest = one_room_pref.preference
                self.fields[field_name].label = "Room Preference"
                self.fields[field_name].initial = chosen

            # TODO: TO BE UNCOMMENTED ONCE A SOLUTION FOR MORE THAN ONE ROOM IS DECIDED
            # rooms_slot_available = Slot.objects.filter(timeslot=timeslot).order_by("room__id")
            # number_of_tutor_rooms = rooms_slot_available.count()
            #
            # if number_of_tutor_rooms == 1:
            #     # Disabled slider for label only purposes, with side feature to say no adjustment available
            #     room = rooms_slot_available.first().room
            #     field_name = 'timeslot_office_preference_%s_%s' % (timeslot.timeslot_id, room.id)
            #     self.fields[field_name] = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'min':0, 'max': 0, 'step': 0}))
            #     self.fields[field_name].label = "%s only" % (str(room), )
            #     self.fields[field_name].disabled = True
            # elif number_of_tutor_rooms == 2:
            #     room_pref, other_room_pref = rooms_slot_available.first().room, rooms_slot_available.last().room
            #     field_name = 'timeslot_office_preference_%s_%s' % (timeslot.timeslot_id, room_pref.room.id)
            #     self.fields[field_name] = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'min':-2, 'max': 2, 'step': 1}))
            #     self.fields[field_name].initial = room_pref.preference
            #     self.fields[field_name].label = str(other_room_pref.room) + " <-> " + str(room_pref.room)
            # else:
            #     for room_slot in rooms_slot_available:
            #         room = room_slot.room
            #         field_name = 'timeslot_office_preference_%s_%s' % (timeslot.timeslot_id, room.id)
            #         self.fields[field_name] = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'min':-2, 'max': 2, 'step': 1}))
            #         self.fields[field_name].initial = room_prefs.get(room=room).preference
            #         self.fields[field_name].label = str(room)

    def save_slot_preference_data(self):
        # TODO: TO BE UNCOMMENTED ONCE A SOLUTION FOR MORE THAN ONE ROOM IS DECIDED
        # number_of_tutor_rooms = Room.objects.count()

        for name, value in self.cleaned_data.items():
            if name.startswith("timeslot_time_preference_"):
                timeslot_id = int(name.replace("timeslot_time_preference_", ""))
                timeslot = TimeSlot.objects.get(timeslot_id=timeslot_id)
                timeslot_pref = TimeSlotPreference.objects.get(
                    timeslot=timeslot, tutor=self.tutor
                )
                timeslot_pref.preference = value
                timeslot_pref.save(update_fields=["preference"])
            elif name.startswith("timeslot_office_preference_"):
                timeslot_id = int(name.replace("timeslot_office_preference_", ""))
                timeslot = TimeSlot.objects.get(timeslot_id=timeslot_id)
                room_prefs = RoomPreference.objects.filter(
                    timeslot=timeslot, tutor=self.tutor
                )

                if value == 0:
                    for one_room_pref in room_prefs:
                        one_room_pref.preference = 0
                        one_room_pref.save(update_fields=["preference"])
                else:
                    for one_room_pref in room_prefs:
                        if one_room_pref.room.id == value - 1:
                            one_room_pref.preference = 2
                        else:
                            one_room_pref.preference = -2
                        one_room_pref.save(update_fields=["preference"])

                # TODO: TO BE UNCOMMENTED ONCE A SOLUTION FOR MORE THAN ONE ROOM IS DECIDED
                # timeslot_id, room_id = [int(v) for v in name.replace("timeslot_office_preference_", "").split("_")]

                # timeslot = TimeSlot.objects.get(timeslot_id=timeslot_id)
                # room_pref_for_timeslot = RoomPreference.objects.filter(timeslot=timeslot, tutor=self.tutor)

                # if number_of_tutor_rooms == 1:
                #     room_pref = room_pref_for_timeslot.first()
                #     assert room_pref.room.id == room_id, "The room ids somehow did not match: {} vs {}".format(room_pref.room.id, room_id)
                #     room_pref.preference = value
                #     room_pref.save(update_fields=["preference"])
                # elif number_of_tutor_rooms == 2:
                #     # For loop used in case the ordering is not correct
                #     for room_pref in room_pref_for_timeslot:
                #         room_pref.preference = value * (1 if (room_pref.room.id == room_id) else -1)
                #         room_pref.save(update_fields=["preference"])
                # else:
                #     # Room IDs sourced from each slider
                #     room_pref = room_pref_for_timeslot.get(room_id=room_id)
                #     room_pref.preference = value
                #     room_pref.save(update_fields=["preference"])
            elif name == "adjacent_pref":
                self.tutor.adjacent_pref = value
            elif name == "num_assignments":
                self.tutor.num_assignments = value
            elif name == "tutor_name":
                self.tutor.name = value
        self.tutor.save(update_fields=["adjacent_pref", "num_assignments", "name"])


class TutoringAlgorithmOutputForm(forms.Form):
    output = forms.FileField(label="Upload tutoring algorithm output file")
