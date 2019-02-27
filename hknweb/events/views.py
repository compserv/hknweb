from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt #doing this for now bc idk how to make csrf work
from django.db.models import F # Avoids changing database values without risking a race condition

from .models import Event, Rsvp
from .forms import EventForm
from hknweb.models import Profile

def index(request):
    events = Event.objects.order_by('-start_time')[:10]
    print(events)
    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)

def show_details(request, id):
    event = Event.objects.get(pk=id)
    rsvp = Rsvp.objects.filter(user=request.user, event=event).exists()
    context = {
        'event': event,
        'rsvp': rsvp,
    }
    if request.user.is_authenticated:
        return render(request, 'events/show_details.html', context)
    return redirect('/events')

@csrf_exempt  #doing this for now bc idk how to make csrf work
def rsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = Event.objects.get(pk=id)
    if request.user.is_authenticated and event.rsvps < event.rsvp_limit:
        event.rsvps = F("rsvps") + 1
        Rsvp.objects.create(user=request.user, event=event)
        messages.success(request, 'RSVP\'d!')
    else:
        messages.error(request, 'Could not RSVP; the RSVP limit has been reached.')
    return redirect('/events/' + str(id))

@csrf_exempt  #doing this for now bc idk how to make csrf work
def unrsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = Event.objects.get(pk=id)
    if request.user.is_authenticated and event.rsvps < event.rsvp_limit:
        #check if rsvp for this event and this user already exists; if false, then set true
        event.rsvps = F("rsvps") - 1
        Rsvp.objects.get(user=request.user, event=event).delete()
        messages.success(request, 'un-RSVP\'d :(')
    else:
        messages.error(request, 'Something went wrong; could not un-RSVP.')
    return redirect('/events/' + str(id))

def add_event(request):
    form = EventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Event has been added!')
            return redirect('/events')
        else:
            print(form.errors)
            messages.success(request, 'Something went wrong oops')
            return render(request, 'events/add_event.html', {'form': EventForm(None)})
    return render(request, 'events/add_event.html', {'form': EventForm(None)})

def show_checklist(request):
    return HttpResponse("Hello, world. You're at the checklist index.")
