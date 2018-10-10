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
	days = Day.objects.order_by('id').all()
	slots_11 = Slot.objects.filter(starttime=11).order_by('day_id').all()
	slots_12 = Slot.objects.filter(starttime=12).order_by('day_id').all()
	slots_1 = Slot.objects.filter(starttime=1).order_by('day_id').all()
	slots_2 = Slot.objects.filter(starttime=2).order_by('day_id').all()
	slots_3 = Slot.objects.filter(starttime=3).order_by('day_id').all()
	slots_4 = Slot.objects.filter(starttime=4).order_by('day_id').all()
	context = {
		'days' : days,
		'slots_11' : slots_11,
		'slots_12' : slots_12,
		'slots_1' : slots_1,
		'slots_2' : slots_2,
		'slots_3' : slots_3,
		'slots_4' : slots_4,
	}
	return render(request, 'tutoring/index.html', context)