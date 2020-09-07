from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.forms import formset_factory
from .models import TimeSlot, Slot, Tutor, Course, TimeSlotPreference, CoursePreference
from .forms import TimeSlotPreferenceForm
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
    }
    return render(request, 'tutoring/index.html', context)
    
# @permission_required('events.add_event', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def tutor_course_preference(request):
    # if request.method == 'POST':
    #     form = ClassPreferenceForm(request.POST or None)
    #     if form.is_valid():
    #         courses = form.cleaned_data.get("courses")
    #         if Tutor.objects.filter(user = request.user).exists():
    #             tutor = Tutor.objects.get(user = request.user)
    #             tutor.courses.set(courses)
    #             tutor.save()
    #         else:
    #             name = request.user.get_full_name()
    #             tutor = Tutor(user = request.user, name = name)
    #             tutor.save()
    #             tutor.courses.set(courses)
    #             tutor.save()
    #         messages.success(request, 'Your course preferences have been successfully updated!')
    #     else:
    #         print(form.errors)
    #         messages.success(request, 'Something went wrong oops')
    # return render(request, 'tutoring/preferences.html', {'form': ClassPreferenceForm(None)})
    return


# @permission_required('events.add_event', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
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
    print(context)
    if request.method == 'POST':
        if form.is_valid():
            form.save_slot_preference_data()
    return render(request, 'tutoring/slotpref.html', context)

def generate_all_slots():
    id = 121
    timeslot_id = 1
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
            
# Generates file that will be fed into algorithm
def prepare_algorithm_input(request):
    if request.method == 'GET':
        return
    return
  
#Take in json data and 
def generate_schedule(request):
    # if request.method == 'POST':
    #     json_data = json.loads(request.body)
    #     id = 121
    #     Slot.objects.all().delete()
    #     for hour, _ in Slot.HOUR_CHOICES:
    #         for day, _ in Slot.DAY_CHOICES:
    #             for office, _ in Slot.ROOM_CHOICES:
    #                 slot = Slot(hour = hour, day = day, room = office, slot_id = id)
    #                 tutor_ids = json_data[slot_id]
    #                 for tutor_id in tutor_ids:
    #                     tutor = Tutor.objects.get(id=tutor_id)
    #                     slot.tutors.add(tutor)
    #                 slot.save()
    #                 id += 1
    # return index(request)
    generate_all_slots()
    
    return index(request)