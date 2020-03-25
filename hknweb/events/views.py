from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views import generic
from functools import wraps

from .models import Event, EventType, Rsvp
from .forms import EventForm

# decorators

# first requires log in, but if you're already logged in but don't have permission, displays more info
def login_and_permission(permission_name):
    def decorator(func):
        return wraps(func)( # preserves function attributes to the decorated function
                login_required(login_url='/accounts/login/')(
                    # raises 403 error which invokes our custom 403.html
                    permission_required(permission_name, login_url='/accounts/login/', raise_exception=True)(
                        func # decorates function with both login_required and permission_required
                    )
                )
            )
    return decorator

def method_login_and_permission(permission_name):
    return method_decorator(login_and_permission(permission_name), name='dispatch')

# views

def index(request):
    events = Event.objects.order_by('-start_time')
    event_types = EventType.objects.order_by('type')

    context = {
        'events': events,
        'event_types': event_types,
    }
    return render(request, 'events/index.html', context)

@login_and_permission('events.view_event')
def show_details(request, id):
    event = get_object_or_404(Event, pk=id)
    rsvps = Rsvp.objects.filter(event=event)
    rsvpd = Rsvp.objects.filter(user=request.user, event=event).exists()
    waitlisted = False
    waitlist_position = 0

    if rsvpd:
        # Gets the rsvp object for the user
        rsvp = Rsvp.objects.filter(user=request.user, event=event)[:1].get()
        # Check if waitlisted
        if event.rsvp_limit:
            rsvps_before = rsvps.filter(created_at__lt = rsvp.created_at).count()
            waitlisted = rsvps_before >= event.rsvp_limit

    # Get waitlist position
    if waitlisted:
        position = rsvps.filter(created_at__lt=rsvp.created_at).count()
        waitlist_position = position - event.rsvp_limit + 1
    # Render only non-waitlisted rsvps
    rsvps = event.admitted_set()
    waitlists = event.waitlist_set()
    limit = event.rsvp_limit
    context = {
        'event': event,
        'rsvpd': rsvpd,
        'rsvps': rsvps,
        'waitlisted': waitlisted,
        'waitlist_position': waitlist_position,
        'waitlists': waitlists,
        'limit': limit,
        'can_edit': request.user.has_perm('events.change_event')
    }
    return render(request, 'events/show_details.html', context)

@login_and_permission('events.add_rsvp')
def rsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = get_object_or_404(Event, pk=id)

    if request.user.is_authenticated and Rsvp.has_not_rsvpd(request.user, event):
        Rsvp.objects.create(user=request.user, event=event, confirmed=False)
    else:
        messages.error(request, 'You have already RSVP\'d.')
    return redirect('/events/' + str(id))

@login_and_permission('events.remove_rsvp')
def unrsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = get_object_or_404(Event, pk=id)
    rsvp = get_object_or_404(Rsvp, user=request.user, event = event)
    if rsvp.confirmed:
        messages.error(request, 'Cannot un-rsvp from event you have gone to.')
    else:
        rsvp.delete()
    return redirect(event)

@login_and_permission('events.add_event')
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
            return render(request, 'events/event_add.html', {'form': EventForm(None)})
    return render(request, 'events/event_add.html', {'form': EventForm(None)})

@method_login_and_permission('events.change_event')
class EventUpdateView(generic.edit.UpdateView):
    model = Event
    fields = ['name', 'slug', 'start_time', 'end_time', 'location', 'event_type',
              'description', 'rsvp_limit']
    template_name_suffix = '_edit'

