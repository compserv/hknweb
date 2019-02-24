from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt #doing this for now bc idk how to make csrf work
from django.db.models import F # Avoids changing database values without risking a race condition

from .models import Event, Rsvp
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
        Rsvp.objects.get(user=request.user, event=event)
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
    event = Event.objects.get(pk=id)

    if request.method == 'POST':
        rsvp = request.user.is_authenticated and event.rsvps < event.rsvp_limit
        # If authenticated and event is under RSVP cap
        if rsvp:
            event.rsvps = F("rsvps") + 1
            Rsvp.objects.create(user=request.user, event=event)
            messages.success(request, 'RSVP\'d!')
        else:
            messages.error(request, 'Could not RSVP; the RSVP limit has been reached.')
        return redirect('/events/' + str(id))
    else:
        return HttpResponse("For some reason, rsvp() was called with an HTTP request that wasn't a POST.")

@csrf_exempt  #doing this for now bc idk how to make csrf work
def unrsvp(request, id):
    event = Event.objects.get(pk=id)

    if request.method == 'POST':
        if request.user.is_authenticated and event.rsvps < event.rsvp_limit:
            #check if rsvp for this event and this user already exists; if false, then set true
            event.rsvps = F("rsvps") - 1
            Rsvp.objects.get(user=request.user, event=event).delete()
            messages.success(request, 'un-RSVP\'d :(')
        else:
            messages.error(request, 'Something went wrong; could not un-RSVP.')
        return redirect('/events/' + str(id))
    else:
        return HttpResponse("For some reason, unrsvp() was called with an HTTP request that wasn't a POST.")
