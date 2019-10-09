from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader, RequestContext
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt #doing this for now bc idk how to make csrf work
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
import datetime
import pytz

from .models import Event, Rsvp
from .forms import EventForm
from hknweb.models import Profile

# decorators

# used for things only officers and candidates can access
def check_account_access(func):
    def check_then_call(request, *args, **kwargs):
        if not is_cand_or_officer(request.user):
            return render(request, "errors/401.html", status=401)
        return func(request, *args, **kwargs)
    return check_then_call

def is_cand_or_officer(user):
    return user.groups.filter(name=settings.CAND_GROUP).exists() or \
           user.groups.filter(name=settings.OFFICER_GROUP).exists()


# views

def index(request):
    events = Event.objects.order_by('-start_time')
    
    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context, RequestContext(request, context))

@login_required(login_url='/accounts/login/')
def show_details(request, id):
    
    event = get_object_or_404(Event, pk=id)

    rsvp = Rsvp.objects.filter(user=request.user, event=event).exists()
    context = {
        'event': event,
        'rsvp': rsvp,
    }
    return render(request, 'events/show_details.html', context)

@csrf_exempt  #doing this for now bc idk how to make csrf work
@login_required(login_url='/accounts/login/')
@check_account_access
def rsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = get_object_or_404(Event, pk=id)
    rsvps = event.rsvp_set.count()

    if request.user.is_authenticated and (event.rsvp_limit is None or rsvps < event.rsvp_limit):
        Rsvp.objects.create(user=request.user, event=event, confirmed=False)
        messages.success(request, 'RSVP\'d!')
    else:
        messages.error(request, 'Could not RSVP; the RSVP limit has been reached.')
    return redirect('/events/' + str(id))

@csrf_exempt  #doing this for now bc idk how to make csrf work
@login_required(login_url='/accounts/login/')
@check_account_access
def unrsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = get_object_or_404(Event, pk=id)

    if request.user.is_authenticated:
        # check if rsvp for this event and this user already exists; if false, then set true
        if datetime.datetime.now().replace(tzinfo=pytz.UTC) > event.end_time.replace(tzinfo=pytz.UTC):
            messages.error(request, 'Could not un-RSVP: the event has already ended.')
        else:
            rsvp = get_object_or_404(Rsvp, user=request.user, event=event)
            rsvp.delete()
            messages.success(request, 'un-RSVP\'d :(')
    else:
        messages.error(request, 'Something went wrong; could not un-RSVP.')
    return redirect('/events/' + str(id))


@permission_required('events.add_event', login_url = '/accounts/login/')
def add_event(request):
    form = EventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event has been added!')
            return redirect('/events')
        else:
            print(form.errors)
            messages.success(request, 'Something went wrong oops')
            return render(request, 'events/add_event.html', {'form': EventForm(None)})
    return render(request, 'events/add_event.html', {'form': EventForm(None)})
