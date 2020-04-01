from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.forms import formset_factory
from .models import Slot, Tutor, Course
from .forms import ClassPreferenceForm 
import json

def index(request):
    days = [name for _, name in Slot.DAY_CHOICES]
    hours = Slot.HOUR_CHOICES
    cory_slots = {hour: Slot.objects.filter(room=Slot.CORY, hour=hour).order_by('hour').order_by('day') for hour, _ in hours}
    soda_slots = {hour: Slot.objects.filter(room=Slot.SODA, hour=hour).order_by('hour').order_by('day') for hour, _ in hours}
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
    print(context)
    return render(request, 'tutoring/index.html', context)

def tutor_slot_preference(request):
    if request.method == 'POST':
        #process form
        return
    SlotPreferenceFormSet = formset_factory()
# @permission_required('events.add_event', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def tutor_course_preference(request):
    if request.method == 'POST':
        form = ClassPreferenceForm(request.POST or None)
        if form.is_valid():
            courses = form.cleaned_data.get("courses")
            if Tutor.objects.filter(user = request.user).exists():
                tutor = Tutor.objects.get(user = request.user)
                tutor.courses.set(courses)
                tutor.save()
            else:
                name = request.user.get_full_name()
                tutor = Tutor(user = request.user, name = name)
                tutor.save()
                tutor.courses.set(courses)
                tutor.save()
            messages.success(request, 'Your course preferences have been successfully updated!')
        else:
            print(form.errors)
            messages.success(request, 'Something went wrong oops')
    return render(request, 'tutoring/preferences.html', {'form': ClassPreferenceForm(None)})


# @permission_required('events.add_event', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def tutor_slot_preference(request):
    return

def prepare_algorithm_input(request):
    if request.method == 'GET':
        

def generate_schedule(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        slot_id = 121
        Slot.objects.all().delete()
        for hour, _ in Slot.HOUR_CHOICES:
            for day, _ in Slot.DAY_CHOICES:
                for office, _ in Slot.ROOM_CHOICES:
                    slot = Slot(hour = hour, day = day, room = room, slot_id = id)
                    tutor_ids = json_data[slot_id]
                    for tutor_id in tutor_ids:
                        tutor = Tutor.objects.get(id=tutor_id)
                        slot.tutors.add(tutor)
                    slot.save()
                    slot_id += 1
    return index(request)