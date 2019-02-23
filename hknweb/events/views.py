from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt #doing this for now bc idk how to make csrf work

from .models import Event, Rsvp
from .forms import EventForm
from hknweb.models import Profile

def index(request):
    events = Event.objects.order_by('-start_time')[:10]
    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)


def show_details(request, id):
    event = Event.objects.get(pk=id)
    try:
        rsvp = Rsvp.objects.get(user=Profile.objects.get(user=request.user), event=event)
        rsvp = True
    except Rsvp.DoesNotExist:
        rsvp = False

    context = {
        'event': event,
        'rsvp': rsvp
    }
    return render(request, 'events/show_details.html', context)

@csrf_exempt  #doing this for now bc idk how to make csrf work
def rsvp(request, id):
    # If authenticated and event is under RSVP cap
    event = Event.objects.get(pk=id)

    print("rsvps:", event.rsvps)
    if request.method == 'POST':
        if request.user.is_authenticated and event.rsvps < event.rsvp_limit:
            event.rsvps += 1
            event.save()
            Rsvp.objects.create(user=Profile.objects.get(user=request.user), event=event)
            messages.success(request, 'RSVP\'d!')
            rsvp = True
        else:
            messages.error(request, 'Could not RSVP; the RSVP limit has been reached.')
            rsvp = False
        context = {
            'event': event,
            'rsvp': rsvp
        }
        return redirect('/events/' + str(id))
    #return render(request, 'events/show_details.html')

@csrf_exempt  #doing this for now bc idk how to make csrf work
def unrsvp(request, id):
    # If authenticated and event is under RSVP cap
    event = Event.objects.get(pk=id)

    print("rsvps:", event.rsvps)
    if request.method == 'POST':
        if request.user.is_authenticated and event.rsvps < event.rsvp_limit:
            #check if rsvp for this event and this user already exists; if false, then set true
            event.rsvps -= 1
            event.save()
            Rsvp.objects.get(user=Profile.objects.get(user=request.user), event=event).delete()
            messages.success(request, 'un-RSVP\'d :(')
            rsvp = False
        else:
            messages.error(request, 'Something went wrong; could not un-RSVP.')
            rsvp = True
        context = {
            'event': event,
            'rsvp': rsvp
        }
        return redirect('/events/' + str(id))
    #return render(request, 'events/show_details.html')

def add_event(request):
    form = EventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Event has been added!')
            return redirect('/events')
        else:
            return render(request, 'events/add_event.html', {'form': EventForm(None)})
    return render(request, 'events/add_event.html', {'form': EventForm(None)})

def show_checklist(request):
    return HttpResponse("Hello, world. You're at the attendance index.")

def future(request):
    return HttpResponse("Hello, world. You're at the future index.")

def past(request):
    return HttpResponse("Hello, world. You're at the past index.")
