from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Event, Rsvp

def index(request):
    events = Event.objects.order_by('-start_time')[:10]
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


def rsvp(request, id):
    # If authenticated and event is under RSVP cap
    event = Event.objects.get(pk=id)
    print("rsvps:", event.rsvps)
    if request.user.is_authenticated and event.rsvps < event.rsvp_limit:
        event.rsvps += 1
        event.save()
        Rsvp.objects.create(event=event)
    return HttpResponse("Hello, world. You're at the rsvp index.")


def future(request):
    return HttpResponse("Hello, world. You're at the future index.")


def past(request):
    return HttpResponse("Hello, world. You're at the past index.")


def rsvps(request):
    return HttpResponse("Hello, world. You're at the rsvps index.")
