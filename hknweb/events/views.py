from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Event

def index(request):
    events = Event.objects.order_by('-start_time')[:10]
    print("This should not be printing.")
    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)


def show_details(request, id):
    event = Event.objects.get(pk=id)
    context = {
        'event': event,
    }
    return render(request, 'events/show_details.html', context)


def future(request):
    return HttpResponse("Hello, world. You're at the future index.")


def past(request):
    return HttpResponse("Hello, world. You're at the past index.")


def rsvps(request):
    return HttpResponse("Hello, world. You're at the rsvps index.")
