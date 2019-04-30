import json

from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.shortcuts import redirect

from hknweb.exams.models import Course
from .models import Slot, CoursePreference, Properties
from .models import Tutor
from .models import Availability
from django.http import JsonResponse


@admin.register(Availability)
class AvailibityAdmin(admin.ModelAdmin):
    list_display = ['tutor__name', 'slot_day', 'slot_hour', 'preference_level']

    def slot_day(self, obj):
        return obj.slot.day

    def slot_hour(self, obj):
        return obj.slot.hour

    def get_name(self, obj):
        return obj.author.name


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    def get_urls(self):
        # get the default urls
        urls = super(TutorAdmin, self).get_urls()
        # define security urls
        additonal_urls = [
            url(r'^update_preferences/$', self.admin_site.admin_view(self.update_preferences)),
            url(r'^gen_course_list/$', self.admin_site.admin_view(self.gen_course_list)),
            url(r'^gen_tutor_course_prefs/$', self.admin_site.admin_view(self.gen_tutor_course_prefs)),
            url(r'^slot_id/$', self.admin_site.admin_view(self.slot_id)),
            url(r'^adj_slots/$', self.admin_site.admin_view(self.adj_slots))
        ]

        # Make sure here you place your added urls first than the admin default urls
        return additonal_urls + urls

    def update_preferences(self, request):

        tutor = request.user.tutor

        preferences_options = {'current': 0, 'completed': 1, 'preferred': 2}
        course_preferences = tutor.coursepreference

        for option, _ in preferences_options.items():
            course_ids = [int(item) for item in request.GET.get(option, '').split() if item != '']
            selected = []
            for course in course_preferences:
                if course.id in course_ids:
                    selected.append(course)

            for pref in selected:
                pref.level = preferences_options[option]
                pref.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated your tutoring preferences")
        courses_added = tutor.courses
        # return redirect('signup_courses')

    def gen_tutor_course_prefs(self):
        course_array = Course.objects.all()
        # Create {"cs61a" : 0, "cs61b" : 1, ...}
        course_indices = {}
        for index, course in enumerate(course_array):
            course_indices[course] = index
        tutor_prefs = {}
        for tutor in Tutor.objects.all():
            course_prefs = [] * len(course_indices)
            for course_pref in tutor.coursepreference:
                course_prefs[course_indices[course_pref.course.course_abbr]] = course_pref.level
            tutor_prefs[tutor.user.id] = course_prefs
        return tutor_prefs

    def slot_id(self, day, hour, office):
        num_hours = len(Slot.HOUR_CHOICES)
        num_days = len(Slot.DAY_CHOICES)

        return (num_hours * (day - 1)) + (hour - Slot.HOUR_CHOICES[0][0]) + (office * num_hours * num_days)

    def adj_slots(self, slot):
        this_slot_id = self.slot_id(slot.day, slot.hour, slot.room)
        hour = slot.hour

        if hour == Slot.HOUR_CHOICES[0][0]:
            return [this_slot_id + 1]
        elif hour == Slot.HOUR_CHOICES[-1][0]:
            return [this_slot_id - 1]
        else:
            return [this_slot_id - 1, this_slot_id + 1]

    def get_tutor_slot_prefs(self, tutor):
        num_times = len(Slot.DAY_CHOICES) * len(Slot.HOUR_CHOICES)
        num_slots = len(Slot.DAY_CHOICES) * len(Slot.HOUR_CHOICES) * len(Slot.ROOM_CHOICES)

        time_prefs = [0] * num_times
        office_prefs = [0] * num_slots  # Cory >> -2, -1, 0, 1, 2 >> Soda
        for availability in tutor.availabilities:
            slot = availability.slot

            this_slot_id = self.slot_id(slot.day, slot.hour, 0 if Slot.CORY == slot.preferred_room else 1)

            office_prefs[this_slot_id] = 1 * availability.room_strength
            # If cory or no pref, set pref to negative
            # (Because EE is currently less popular than CS)
            if slot.preferred_room == Slot.CORY:
                office_prefs[this_slot_id] *= -1

            office_prefs[(this_slot_id + num_times) % num_slots] = -1 * office_prefs[this_slot_id]
            time_prefs[this_slot_id] = slot.preference_level  # Either 1 or 2... I think...
            time_prefs[(this_slot_id + num_times) % num_slots] = time_prefs[this_slot_id]
        return time_prefs, office_prefs

    def num_slot_assignments(self, tutor):
        if tutor.user.groups.name == "officer":
            return 2
        elif tutor.user.groups.name == "cmember":
            return 1
        else:
            return 0

    def params_for_scheduler(self, randomSeed='False', maximumCost='0', machineNum='False', patience='False'):
        # Room 0 = Cory; Room 1 = Soda
        # Adjacency -1 = Does not want adjacent, 0 = Don't care, 1 = Wants adjacent

        course_list = Course.objects.all()
        cory_course_pref = [(course.department == 'EE') for course in course_list]
        soda_course_pref = [(course.department == 'CS') for course in course_list]
        all_tutors = []
        tutor_course_prefs = self.gen_tutor_course_prefs()
        for tutor in Tutor.objects.all():
            tutor_slot_prefs = self.get_tutor_slot_prefs(tutor)
            tutor_obj = {
                "tid": tutor.user.id,
                'name': tutor.user.get_full_name(),
                "timeSlots": tutor_slot_prefs[0],
                'officePrefs': tutor_slot_prefs[1],
                'courses': tutor_course_prefs[tutor.user.id],
                'adjacentPref': tutor.adjacency,
                'numAssignments': self.num_slot_assignments(tutor)
            }
            all_tutors.append(tutor_obj)
        all_slots = []
        for slot in Slot.objects.all():
            office_course_prefs = (cory_course_pref if slot.room == Slot.CORY else soda_course_pref)
            this_slot_id = self.slot_id(slot.day, slot.hour, slot.room)
            slot_obj = {
                'sid': this_slot_id,
                'name': 'InternalSlot' + slot.id.to_s,
                'adjacentSlotIDs': self.adj_slots(slot),
                'courses': office_course_prefs,
                'day': slot.day,
                'hour': slot.hour,
                'office': slot.room
            }
            all_slots.append(slot_obj)
        ret = {
            'courseName': course_list,
            'tutors': all_tutors,
            'slots': all_slots
        }
        return JsonResponse(ret)

    def update_schedule(self, request):
        errors = []
        if request.GET.get('commit', '') == "Save changes":
            changed = False
            for slot in Slot.objects.all():
                room = slot.room
                day = slot.day
                hour = slot.hour
                new_assignments = request.get('assignments')[room][day][hour]
                new_assignments = [Tutor.objects.get(i) for i in new_assignments]
                slot_tutors = slot.tutors
                for tutor in slot_tutors:
                    if tutor not in new_assignments:
                        slot.tutors.delete(tutor)
                        changed = True

                for tutor in new_assignments:
                    if tutor not in slot_tutors:
                        slot.tutors.append(tutor)
                        changed = True
                if slot:
                    slot.save()
        elif request.get('commit', '') == "Reset all":
            changed = True
            for slot in Slot.objects.all():
                slot.tutors = []
                slot.save()
        else:
            messages.add_message(request, messages.MessageFailure, 'Invalid Action')
            return redirect("edit_schedule")

        all_tutors = request.get('only_available', None)
        if changed:
            messages.add_message(request, messages.SUCCESS, "Tutoring schedule updated.")
        elif not all_tutors:
            messages.add_message(request, messages.SUCCESS, "Tutors shown for all slots.")
        else:
            messages.add_message(request, messages.SUCCESS, "Nothing changed in the tutoring schedule.")
        messages.add_message(request, messages.MessageFailure, ''.join(errors))

        return redirect("edit_schedule", all_tutors=all_tutors)


def json_update(self, request):
    json_str = request.GET.get('json_str', '')
    json_dic = {}
    try:
        json_dic = json.loads(json_str)
    except:
        messages.add_message(request, messages.MessageFailure, 'JSON parse failed')
    errors = []
    changed = False
    for id, person_ids in json_dic.items():
        new_assignments = [User.objects.get(x).tutor for x in person_ids]
        slot = Slot.objects.get(id)
        if not slot:
            errors.append("Invalid slot id: " + str(id))
        slot_tutors = slot.tutors
        for tutor in slot_tutors:
            if tutor not in new_assignments:
                slot.tutors.remove(tutor)
                changed = True
        for assignment in new_assignments:
            if assignment not in slot.tutors:
                slot.tutors.append(assignment)
                changed = True
        if slot:
            slot.save()
    if changed:
        messages.add_message(request, messages.SUCCESS, "Tutoring schedule updated.")
    else:
        messages.add_message(request, messages.SUCCESS, "Nothing changed in the tutoring schedule.")
    if errors:
        messages.add_message(request, messages.MessageFailure, ' ' + ''.join(errors))
    return redirect('edit_schedule')


def upload_schedule(self):
    pass


def settings(self):
    pass


def find_courses(self):
    pass


def add_course(self):
    pass


def authorize_tutoring_signup(self, tutor):
    return tutor.user.groups.name == "officer" or tutor.user.groups.name == "cmember" or tutor.user.groups.name == "assistant"


def compute_stats(self):
    stats = {
        "officer": {},
        "cmember": {}
    }
    happiness_total = {
        "officer": 0,
        "cmember": 0
    }
    for tutor in Tutor.objects.all():
        happiness = 0
        first_choice = 0
        second_choice = 0
        adjacencies = 0
        correct_office = 0
        wrong_assign = 0
        for slot in tutor.slots:
            av = Availability.objects.filter(tutor__id=tutor.id, slots__day=slot.day, slots__hour=slot.hour)
            if not av:
                wrong_assign += 1
            elif av.preference_level == Availability.preferred:
                first_choice += 1
            elif av.preference_level == Availability.available:
                second_choice += 1
            else:
                raise ValueError("Availability with preference level of unavailable? Contradiction!?")
            if av:
                if slot.room == av.slots.room or av.room_strength == 0:
                    correct_office += 2
                elif av.room_strength == 1:
                    correct_office += 1
            adj_closed_list = []
            if tutor.adjacency != 0 and tutor.person:
                for other_slot in tutor.slots:
                    if other_slot not in adj_closed_list:
                        if slot.adjacent_to(other_slot):
                            if tutor.adjacency == 1 or tutor.adjacency == 0:
                                adjacencies += 1
                        elif tutor.adjacency == -1 or tutor.adjacency == 0:
                            adjacencies += 1
            adj_closed_list.append(slot)

        happiness += 6 * first_choice - 10000 * wrong_assign + adjacencies + 2 * correct_office
        if tutor.user.groups.name == "officer":
            position = "officer"
            stats_vector = [tutor.availabilities.count, first_choice, second_choice, wrong_assign, adjacencies,
                            correct_office, happiness]
        elif tutor.groups.name == "cmember":
            position = "cmember"
            stats_vector = [tutor.availabilities.count, first_choice, second_choice, wrong_assign, correct_office,
                            happiness]
        else:
            raise ValueError("Not an officer or cmember!")
        stats[position][tutor] = stats_vector
        happiness_total[position] += happiness
    return stats, happiness_total


admin.site.register(CoursePreference)
admin.site.register(Slot)
