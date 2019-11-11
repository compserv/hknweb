from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

from .models import Event, Rsvp
from .forms import EventForm

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
    Event.objects.all()

    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)

@login_required(login_url='/accounts/login/')
@check_account_access
def show_details(request, id):

    event = get_object_or_404(Event, pk=id)

    rsvpd = Rsvp.objects.filter(user=request.user, event=event).exists()
    rsvps = Rsvp.objects.filter(event=event)
    limit = event.rsvp_limit
    rsvps = event.admitted_set()
    waitlist = event.waitlist_set()
    context = {
        'event': event,
        'rsvpd': rsvpd,
        'rsvps': rsvps,
        'limit': limit,
        'waitlist': waitlist,
    }
    return render(request, 'events/show_details.html', context)

@login_required(login_url='/accounts/login/')
@check_account_access
def rsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = get_object_or_404(Event, pk=id)
    rsvps = event.rsvp_set.count()

    # Allow rsvps beyond cap (just waitlist them)
    Rsvp.objects.create(user=request.user, event=event, confirmed=False)
    return redirect('/events/' + str(id))

@login_required(login_url='/accounts/login/')
@check_account_access
def unrsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = get_object_or_404(Event, pk=id)

    if timezone.now() > event.end_time:
        messages.error(request, 'Could not un-RSVP: the event has already ended.')
    else:
        rsvp = get_object_or_404(Rsvp, user=request.user, event=event)
        rsvp.delete()
    return redirect(event)


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
