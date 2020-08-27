from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404, reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.utils import timezone

from hknweb.utils import login_and_permission, method_login_and_permission, get_rand_photo,\
                         get_semester_bounds, DATETIME_12_HOUR_FORMAT
from .constants import GCAL_INVITE_TEMPLATE_ATTRIBUTE_NAME
from .models import Event, EventType, Rsvp
from .forms import EventForm, EventUpdateForm
from .utils import create_gcal_link

# views

def index(request):
    events = Event.objects.order_by('-start_time')
    event_types = EventType.objects.order_by('type')

    context = {
        'events': events,
        'event_types': event_types,
    }
    return render(request, 'events/index.html', context)

@method_login_and_permission('events.add_rsvp')
class AllRsvpsView(TemplateView):
    """ List of rsvp'd and not rsvp'd events. """
    template_name = 'events/all_rsvps.html'

    def get_context_data(self):
        view_option = self.request.GET.get('option')
        semester_start, semester_end = get_semester_bounds(timezone.now())
        all_events = Event.objects \
                .filter(start_time__gte=semester_start) \
                .filter(start_time__lte=semester_end) \
                .order_by('start_time')
        if view_option == "upcoming":
            all_events = all_events.filter(start_time__gte=timezone.now())
        rsvpd_event_ids = Rsvp.objects \
                .filter(user__exact=self.request.user) \
                .values_list('event', flat=True)
        rsvpd_events = all_events \
                .filter(pk__in=rsvpd_event_ids)
        not_rsvpd_events = all_events \
                .exclude(pk__in=rsvpd_event_ids)

        for event in rsvpd_events:
            event.waitlisted = event.on_waitlist(self.request.user) # Is this bad practice? idk

        event_types = EventType.objects.order_by('type')
        context = {
            'rsvpd_events': rsvpd_events,
            'not_rsvpd_events': not_rsvpd_events,
            'event_types': event_types,
        }
        return context

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
    gcal_link = create_gcal_link(event)
    context = {
        'event': event,
        'rsvpd': rsvpd,
        'rsvps': rsvps,
        'waitlisted': waitlisted,
        'waitlist_position': waitlist_position,
        'waitlists': waitlists,
        'limit': limit,
        'can_edit': request.user.has_perm('events.change_event'),
        GCAL_INVITE_TEMPLATE_ATTRIBUTE_NAME: gcal_link,
    }
    return render(request, 'events/show_details.html', context)

@login_and_permission('events.add_rsvp')
def rsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = get_object_or_404(Event, pk=id)

    if Rsvp.has_not_rsvpd(request.user, event):
        Rsvp.objects.create(user=request.user, event=event, confirmed=False)
    else:
        messages.error(request, 'You have already RSVP\'d.')
    next_page = request.POST.get('next', '/')
    return redirect(next_page)

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
        for off_waitlist_rsvp in event.newly_off_waitlist_rsvps(old_admitted):
            send_off_waitlist_email(request, off_waitlist_rsvp.user, event)
    next_page = request.POST.get('next', '/')
    return redirect(next_page)

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
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name_suffix = '_edit'

    def get_initial(self):
        """ Override some prepopulated data with custom data; in this case, make times
            the right format. """
        initial = super().get_initial()
        initial['start_time'] = self.object.start_time.strftime(DATETIME_12_HOUR_FORMAT)
        initial['end_time'] = self.object.end_time.strftime(DATETIME_12_HOUR_FORMAT)
        return initial

    def form_valid(self, form):
        if 'rsvp_limit' in form.changed_data:
            messages.success(self.request, "People who rsvp'd or are on the waitlist are not notified"
                        " when you change the rsvp limit. Be sure to make an announcement!")
        return super().form_valid(form)

# Helpers

def send_off_waitlist_email(request, user, event):
    subject = '[HKN] You have gotten off the waitlist for your event'

    event_link = request.build_absolute_uri(
            reverse("events:detail", kwargs={ 'id': event.id }))
    html_content = render_to_string(
        'events/off_waitlist_email.html',
        {
            'subject': subject,
            'event_name': event.name,
            'event_link': event_link,
            'img_link': get_rand_photo(),
        }
    )
    msg = EmailMultiAlternatives(subject, subject,
                settings.NO_REPLY_EMAIL, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
