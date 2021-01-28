from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import JsonResponse
from hknweb.coursesemester.models import Course
from .models import TimeSlot, Slot, Tutor, TutorCourse, TimeSlotPreference, CoursePreference, Room
from .forms import TimeSlotPreferenceForm, CoursePreferenceForm, TutoringAlgorithmOutputForm
import json

def index(request):
    if Room.objects.all().count() == 0:
        generate_all_rooms()
    if Slot.objects.all().count() == 0:
        generate_all_slots()
    if TutorCourse.objects.all().count() == 0:
        generate_all_courses()
    days = [name for _, name in TimeSlot.DAY_CHOICES]
    hours = TimeSlot.HOUR_CHOICES
    offices = []
    for room in Room.objects.all():
        slot = {hour: Slot.objects.filter(room=room, timeslot__hour=hour).order_by('timeslot__hour').order_by('timeslot__day') for hour, _ in hours}
        office = {
                'room': str(room),
                'slots': slot,
            }
        offices.append(office)
    
    context = {
        
        'days': days,
        'hours': hours,
        'offices': offices,
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
        'hours': TimeSlot.HOUR_CHOICES,
        'message': ""
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save_slot_preference_data()
            context['message'] = "Sign up form saved! (Don't forget to screenshot your selections)"
        else:
            context['message'] = "An error occured, please screenshot your current entries and contact CompServ"
    return render(request, 'tutoring/slotpref.html', context)

def generate_all_rooms():
    for rooms in Room.DEFAULT_ROOM_CHOICES:
        room_model = Room(id=rooms[0], building=rooms[1], room_num=rooms[2])
        room_model.save()

def generate_all_courses():
    for course in Course.objects.all():
        tutor_course = TutorCourse(course=course)
        tutor_course.save()

def generate_all_slots():
    id = 0
    timeslot_id = 0
    room_querySet = Room.objects.all()
    for hour, _ in TimeSlot.HOUR_CHOICES:
        for day, _ in TimeSlot.DAY_CHOICES:
            timeslot = TimeSlot(hour=hour, day=day, timeslot_id = timeslot_id)
            timeslot_id += 1
            timeslot.save()
            for room in room_querySet:
                slot = Slot(timeslot=timeslot, room = room, slot_id = id)
                slot.save()
                id += 1

def initialize_slot_preferences(tutor):
    for timeslot in TimeSlot.objects.all():
        pref = TimeSlotPreference(tutor=tutor, timeslot=timeslot)
        pref.save()

def initialize_course_preferences(tutor):
    for course in TutorCourse.objects.all():
        pref = CoursePreference(tutor=tutor, course=course)
        pref.save()

def get_office_course_preferences(office):
    courses = TutorCourse.objects.all()
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
    input_data = {}
    courses = []
    for course in TutorCourse.objects.all():
        courses.append(str(course.course))
    input_data["courseName"] = courses
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
    input_data["tutors"] = tutors
    slots = []
    cory_course_prefs = get_office_course_preferences(0)
    soda_office_prefs = get_office_course_preferences(1)
    time_gaps = get_slot_time_gaps()
    for slot in Slot.objects.all().order_by('slot_id'):
        slot_dict = {}
        slot_dict["sid"] = slot.slot_id
        slot_dict["name"] = "Slot {}".format(slot.slot_id)
        slot_dict["adjacentSlotIDs"] = get_adjacent_slot_ids(slot, time_gaps)
        if slot.room == 0:
            slot_dict["courses"] = cory_course_prefs
        else:
            slot_dict["courses"] = soda_office_prefs
        slot_dict["day"] = slot.timeslot.get_day()
        slot_dict["hour"] = slot.timeslot.hour
        slot_dict["office"] = slot.get_office()
        slots.append(slot_dict)
    input_data["slots"] = slots
    return JsonResponse(input_data)

def get_day_range_dict(time_gaps, day, slot_hour, last_hour):
    if day not in time_gaps:
        time_gaps[day] = {}
    
    day_range_dict = time_gaps[day]

    if slot_hour not in day_range_dict:
        day_range_dict[slot_hour] = {"Before" : False, "After" : False}
    if last_hour not in day_range_dict:
        day_range_dict[last_hour] = {"Before" : False, "After" : False}
    
    return day_range_dict

def get_slot_time_gaps():
    time_gaps = {} # Day : {Hour : {"Before" : bool, "After" : bool}}
    last_day = -1 # Days of the week: 0 to 6, Sunday to Saturday (see tutoring/models.py)
    last_hour = -1
    for slot in Slot.objects.all().order_by('timeslot__day', 'timeslot__hour'):
        if last_day != slot.timeslot.day:
            if last_hour != -1 and last_day != -1:
                day_range_dict = get_day_range_dict(time_gaps, last_day, slot.timeslot.hour, last_hour)
                day_range_dict[last_hour]["After"] = True

            last_day = slot.timeslot.day
            last_hour = -1
            
        if last_hour == -1:
            last_hour = slot.timeslot.hour
            day_range_dict = get_day_range_dict(time_gaps, slot.timeslot.day, slot.timeslot.hour, last_hour)
            day_range_dict[last_hour]["Before"] = True
            continue
        if last_hour + 1 != slot.timeslot.hour:
            # Otherwise, there is a break in time (note that times should have been sorted)
            # Get the boolean dictionary (pass-by-refs anyway), or make a new one
            day_range_dict = get_day_range_dict(time_gaps, slot.timeslot.day, slot.timeslot.hour, last_hour)
            
            day_range_dict[slot.timeslot.hour]["Before"] = True
            day_range_dict[last_hour]["After"] = True
        
        last_hour = slot.timeslot.hour
    if last_hour != -1 and last_day != -1:
        day_range_dict = get_day_range_dict(time_gaps, last_day, slot.timeslot.hour, last_hour)
        day_range_dict[last_hour]["After"] = True
    return time_gaps

def get_adjacent_slot_ids(slot, time_gaps):
    # row_interval = 2 * len(TimeSlot.DAY_CHOICES)
    # hours_threshold = (len(TimeSlot.HOUR_CHOICES) - 1) * row_interval
    # time_gaps = {Day : {Hour : {"Before" : bool, "After" : bool}}}
    adjacent = []

    gap_before = time_gaps.get(slot.timeslot.day, {}).get(slot.timeslot.hour, {}).get("Before", False)
    gap_after  = time_gaps.get(slot.timeslot.day, {}).get(slot.timeslot.hour, {}).get("After", False)

    if gap_after and (not gap_before):
        adjacent.append(slot.get_previous_hour_slot().slot_id)
    elif gap_before and (not gap_after):
        adjacent.append(slot.get_after_hour_slot().slot_id)
    elif (not gap_before) and (not gap_after):
        adjacent.append(slot.get_previous_hour_slot().slot_id)
        adjacent.append(slot.get_after_hour_slot().slot_id)
    else:
        # Gap on both directions
        # Adjacent will be empty
        pass
    return adjacent

def get_adjacent_times():
    Slot.objects.all()

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