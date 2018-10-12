from django.shortcuts import render

from .models import Slot


def index(request):
    days = [name for _, name in Slot.DAY_CHOICES]
    hours = Slot.HOURS
    cory_slots = {hour: Slot.objects.filter(room=Slot.CORY, hour=hour).order_by('day') for hour in Slot.HOURS}
    soda_slots = {hour: Slot.objects.filter(room=Slot.SODA, hour=hour).order_by('day') for hour in Slot.HOURS}
    context = {
        'days': days,
        'hours': hours,
        'cory_slots': cory_slots,
        'soda_slots': soda_slots,
    }
    return render(request, 'tutoring/index.html', context)
