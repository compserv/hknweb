from django.shortcuts import render

from hknweb import forms
from .models import Slot


def index(request):
    days = [name for _, name in Slot.DAY_CHOICES]
    hours = Slot.HOUR_CHOICES
    cory_slots = {hour: Slot.objects.filter(room=Slot.CORY, hour=hour).order_by('day') for hour, _ in hours}
    soda_slots = {hour: Slot.objects.filter(room=Slot.SODA, hour=hour).order_by('day') for hour, _ in hours}
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

