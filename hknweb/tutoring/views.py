from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import JsonResponse
from .models import TimeSlot, Slot, Tutor, Course, TimeSlotPreference, CoursePreference
from .forms import TimeSlotPreferenceForm, CoursePreferenceForm, TutoringAlgorithmOutputForm
import json

def index(request):
    if Slot.objects.all().count() == 0:
        generate_all_slots()
    days = [name for _, name in TimeSlot.DAY_CHOICES]
    hours = TimeSlot.HOUR_CHOICES
    cory_slots = {hour: Slot.objects.filter(room=Slot.CORY, timeslot__hour=hour).order_by('timeslot__hour').order_by('timeslot__day') for hour, _ in hours}
    soda_slots = {hour: Slot.objects.filter(room=Slot.SODA, timeslot__hour=hour).order_by('timeslot__hour').order_by('timeslot__day') for hour, _ in hours}
    context = {
        'days': days,
        'hours': hours,
        'offices': [
            {
                'room': '290 Cory',
                'slots': cory_slots,
            },
            {
                'room': '345 Soda',
                'slots': soda_slots,
            },
        ],
        'form': TutoringAlgorithmOutputForm()
    }
    return render(request, 'tutoring/index.html', context)
    
@permission_required('tutoring.add_timeslotpreference', login_url='/accounts/login/')
def tutor_course_preference(request):
    if Tutor.objects.filter(user = request.user).exists():
        tutor = Tutor.objects.get(user=request.user)
    else:
        name = request.user.get_full_name()
        tutor = Tutor(user = request.user, name = name)
        tutor.save()
    if CoursePreference.objects.filter(tutor=tutor).count() == 0:
        initialize_course_preferences(tutor)
    form = CoursePreferenceForm(request.POST or None, tutor=tutor)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save_course_preference_data()
    return render(request, 'tutoring/coursepref.html', context)

@permission_required('tutoring.add_timeslotpreference', login_url='/accounts/login/')
def tutor_slot_preference(request):
    if Tutor.objects.filter(user = request.user).exists():
        tutor = Tutor.objects.get(user=request.user)
    else:
        name = request.user.get_full_name()
        tutor = Tutor(user = request.user, name = name)
        tutor.save()
    if TimeSlotPreference.objects.filter(tutor=tutor).count() == 0:
        initialize_slot_preferences(tutor)
    form = TimeSlotPreferenceForm(request.POST or None, tutor=tutor)
    context = {
        'form': form,
        'days': [name for _, name in TimeSlot.DAY_CHOICES],
        'hours': TimeSlot.HOUR_CHOICES
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save_slot_preference_data()
    return render(request, 'tutoring/slotpref.html', context)

def generate_all_slots():
    id = 0
    timeslot_id = 0
    for hour, _ in TimeSlot.HOUR_CHOICES:
        for day, _ in TimeSlot.DAY_CHOICES:
            timeslot = TimeSlot(hour=hour, day=day, timeslot_id = timeslot_id)
            timeslot_id += 1
            timeslot.save()
            for office, _ in Slot.ROOM_CHOICES:
                slot = Slot(timeslot=timeslot, room = office, slot_id = id)
                slot.save()
                id += 1

def initialize_slot_preferences(tutor):
    for timeslot in TimeSlot.objects.all():
        pref = TimeSlotPreference(tutor=tutor, timeslot=timeslot)
        pref.save()

def initialize_course_preferences(tutor):
    for course in Course.objects.all():
        pref = CoursePreference(tutor=tutor, course=course)
        pref.save()

def get_office_course_preferences(office):
    courses = Course.objects.all()
    prefs = []
    #Cory
    if office == 0:
        for course in courses:
            prefs.append(course.cory_preference)
    #Soda
    elif office == 1:
        for course in courses:
            prefs.append(course.soda_preference)
    return prefs

# Generates file that will be fed into algorithm
@permission_required('tutoring.add_slot', login_url='/accounts/login/')
def prepare_algorithm_input(request):
    input = {}
    courses = []
    for course in Course.objects.all():
        courses.append(course.name)
    input["courseName"] = courses
    tutors = []
    for tutor in Tutor.objects.all():
        tutor_dict = {}
        tutor_dict["tid"] = tutor.id
        tutor_dict["name"] = tutor.name
        slot_time_prefs = []
        slot_office_prefs = []
        slot_opposite_office_prefs = []
        for pref in tutor.get_slot_preferences():
            slot_time_prefs.append(pref.time_preference)
            slot_office_prefs.append(pref.office_preference)
            slot_opposite_office_prefs.append(-pref.office_preference)
        tutor_dict["timeSlots"] = slot_time_prefs + slot_time_prefs
        tutor_dict["officePrefs"] = slot_office_prefs + slot_opposite_office_prefs
        course_prefs = []
        for pref in tutor.get_course_preferences():
            course_prefs.append(pref.preference)
        tutor_dict["courses"] = course_prefs
        tutor_dict["adjacentPref"] = tutor.adjacent_pref
        tutor_dict["numAssignments"] = tutor.num_assignments
        tutors.append(tutor_dict)
    input["tutors"] = tutors
    slots = []
    cory_course_prefs = get_office_course_preferences(0)
    soda_office_prefs = get_office_course_preferences(1)
    for slot in Slot.objects.all().order_by('slot_id'):
        slot_dict = {}
        slot_dict["sid"] = slot.slot_id
        slot_dict["name"] = "Slot {}".format(slot.slot_id)
        slot_dict["adjacentSlotIDs"] = get_adjacent_slot_ids(slot.slot_id)
        if slot.room == 0:
            slot_dict["courses"] = cory_course_prefs
        else:
            slot_dict["courses"] = soda_office_prefs
        slot_dict["day"] = slot.timeslot.get_day()
        slot_dict["hour"] = slot.timeslot.hour
        slot_dict["office"] = slot.get_office()
        slots.append(slot_dict)
    input["slots"] = slots
    return JsonResponse(input)

def get_adjacent_slot_ids(slot_id):
    adjacent = []
    if slot_id < 10:
        adjacent.append(slot_id + 10)
    elif slot_id >= 50:
        adjacent.append(slot_id - 10)
    else:
        adjacent.append(slot_id + 10)
        adjacent.append(slot_id + 10)
    return adjacent

@permission_required('tutoring.add_slot', login_url='/accounts/login/')
def generate_schedule(request):
    if request.method == 'POST':
        form = TutoringAlgorithmOutputForm(request.POST, request.FILES)
        if form.is_valid():
            output = request.FILES['output']
            data = json.loads(output.read().decode("utf-8"))
            for slot_id in data:
                slot = Slot.objects.get(slot_id=slot_id)
                tutor_ids = data[slot_id]
                for id in tutor_ids:
                    tutor = Tutor.objects.get(id=id)
                    slot.tutors.add(tutor)
    return redirect('/tutoring/')