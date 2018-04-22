from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Tutor
from .models import Day
from .models import Slot



def future(request):
    return HttpResponse("Hello, world. You're at the future index.")


def past(request):
    return HttpResponse("Hello, world. You're at the past index.")

def index(request):
	days = Day.objects.order_by('id')
	#slots_per_day = [day.slot_set.all().order_by('starttime') for day in days]
	monday_slots = Day.objects.get(id=0).slot_set.order_by('starttime')
	slotcount = Slot.objects.count()
	#for i in range(0,slotcount):
	#	tutors_per_slot +=  [Slot.objects.get(id=i).tutor_set.all()]

	context = {
		'days' : days,
		#'slots_per_day' : slots_per_day,
		#'tutors_per_slot' : tutors_per_slot,
		'monday_slots' : monday_slots,

	}
	return render(request, 'tutoring/index.html', context)