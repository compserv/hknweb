from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import generic

from hknweb.utils import login_and_permission, method_login_and_permission
from .models import Event, EventType, Rsvp
from .forms import EventForm

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

@login_and_permission('events.delete_rsvp')
def unrsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = get_object_or_404(Event, pk=id)
    rsvp = get_object_or_404(Rsvp, user=request.user, event=event)
    if rsvp.confirmed:
        messages.error(request, 'Cannot un-rsvp from event you have gone to.')
    else:
        old_admitted = set(event.admitted_set())
        rsvp.delete()
        event.check_newly_off_waitlist(old_admitted)
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

    def form_valid(self, form):
        if 'rsvp_limit' in form.changed_data:
            messages.success(self.request, "People who rsvp'd or are on the waitlist are not notified"
                        " when you change the rsvp limit. Be sure to make an announcement!")
        return super().form_valid(form)
