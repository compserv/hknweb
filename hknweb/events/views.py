from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import get_object_or_404, reverse
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.core.validators import URLValidator
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.utils import timezone

from markdownx.utils import markdownify

from hknweb.utils import login_and_permission, method_login_and_permission, get_rand_photo,\
                         get_semester_bounds, DATETIME_12_HOUR_FORMAT
from .constants import (
    ACCESSLEVEL_TO_DESCRIPTION,
    ATTR,
    GCAL_INVITE_TEMPLATE_ATTRIBUTE_NAME,
    RSVPS_PER_PAGE,
)
from .models import Event, EventType, Rsvp
from .forms import EventForm, EventUpdateForm
from .utils import (
    create_event,
    create_gcal_link,
    generate_recurrence_times,
    get_access_level,
    get_padding,
)

# views

def index(request):
    events = Event.objects.order_by('-start_time').filter(access_level__gte=get_access_level(request.user))
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
                .filter(access_level__gte=get_access_level(self.request.user)) \
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

        event_types = EventType.objects.order_by('type').all()
        event_types = sorted(event_types, key=lambda e: not (e.type == ATTR.MANDATORY))

        rsvpd_data, not_rsvpd_data = [], []
        for event_type in event_types:
            typed_rsvpd_events = rsvpd_events.filter(event_type=event_type)
            typed_not_rsvpd_events = not_rsvpd_events.filter(event_type=event_type)

            rsvpd_padding, not_rsvpd_padding = get_padding(len(typed_not_rsvpd_events), len(typed_rsvpd_events))

            rsvpd_data.append({
                ATTR.EVENT_TYPE: event_type,
                ATTR.EVENTS: [
                    [event, reverse("events:unrsvp", args=[event.id])]
                    for event in typed_rsvpd_events
                ],
                ATTR.PADDING: rsvpd_padding,
            })
            not_rsvpd_data.append({
                ATTR.EVENT_TYPE: event_type,
                ATTR.EVENTS: [
                    [event, reverse("events:rsvp", args=[event.id])]
                    for event in typed_not_rsvpd_events
                ],
                ATTR.PADDING: not_rsvpd_padding,
            })

        data = [
            {
                ATTR.CLASS: "right-half",
                ATTR.TITLE: "RSVP'd / Waitlist",
                ATTR.EVENTS_DATA: rsvpd_data,
                ATTR.DISPLAY_VALUE: "un-RSVP",
            },
            {
                ATTR.CLASS: "left-half",
                ATTR.TITLE: "Not RSVP'd",
                ATTR.EVENTS_DATA: not_rsvpd_data,
                ATTR.DISPLAY_VALUE: "RSVP",
            },
        ]

        context = {
            ATTR.DATA: data,
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

    event_location = event.location
    url_validator = URLValidator()
    try:
        url_validator(event_location)
        event_location = "<a href='{link}'> {link} </a>".format(link=event_location)
    except:
        pass

    rsvps_page = Paginator(rsvps, RSVPS_PER_PAGE).get_page(request.GET.get("rsvps_page"))
    waitlists_page = Paginator(waitlists, RSVPS_PER_PAGE).get_page(request.GET.get("waitlists_page"))

    access_level = ACCESSLEVEL_TO_DESCRIPTION[get_access_level(request.user)]

    data = [
        {
            ATTR.TITLE: "RSVPs",
            ATTR.DATA: rsvps_page if len(rsvps_page) > 0 else None,
            ATTR.PAGE_PARAM: "rsvps_page",
            ATTR.COUNT: str(rsvps.count()) + " / {limit}".format(limit=limit),
        },
    ]
    if limit:
        data.append(
            {
                ATTR.TITLE: "Waitlist",
                ATTR.DATA: waitlists_page if len(waitlists_page) > 0 else None,
                ATTR.PAGE_PARAM: "waitlists_page",
                ATTR.COUNT: str(waitlists.count()),
            }
        )

    context = {
        ATTR.DATA: data,
        'event': event,
        "event_description": markdownify(event.description),
        "event_location": event_location,
        "access_level": access_level,
        'rsvpd': rsvpd,
        'waitlisted': waitlisted,
        'waitlist_position': waitlist_position,
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
            data = form.cleaned_data

            times = generate_recurrence_times(
                data[ATTR.START_TIME],
                data["end_time"],
                data["recurring_num_times"],
                data["recurring_period"],
            )

            for start_time, end_time in times:
                create_event(data, start_time, end_time, request.user)

            messages.success(request, 'Event has been added!')
            return redirect('/events')
        else:
            messages.error(request, "Something went wrong oops")
    return render(request, "events/event_add.html", {"form": EventForm(None)})

def confirm_rsvp(request, id, operation):
    if request.method != 'POST':
        raise Http404()

    access_level = get_access_level(request.user)
    if access_level > 0:
        raise HttpResponseForbidden()

    rsvp = Rsvp.objects.get(id=id)
    rsvp.confirmed = operation == 0  # { confirmed: 0, unconfirmed: 1 }
    rsvp.save()

    next_page = request.POST.get('next', '/')
    return redirect(next_page)

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
