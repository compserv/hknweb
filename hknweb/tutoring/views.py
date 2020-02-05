from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Slot, Tutor, Course
from .forms import ClassPreferenceForm


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

# @permission_required('events.add_event', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def tutor_class_preference(request):
    form = ClassPreferenceForm(request.POST or None)
    if request.method == 'POST':
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


def generate_schedule(request):
    Slot.objects.all().delete()
    for room, _ in Slot.ROOM_CHOICES:
        for day, _ in Slot.DAY_CHOICES:
            for hour, _ in Slot.HOUR_CHOICES:
                print(room, day, hour)
                slot = Slot(hour = hour, day = day, room = room)
                slot.save()
    return index(request)