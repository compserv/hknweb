from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Event

def index(request):
    events = Event.objects.order_by('-created_at')[:10]

    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)


def future(request):
    return HttpResponse("Hello, world. You're at the future index.")


def past(request):
    return HttpResponse("Hello, world. You're at the past index.")


def rsvps(request):
    return HttpResponse("Hello, world. You're at the rsvps index.")
