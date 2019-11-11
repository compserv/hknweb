from django.db import models
from django.contrib.auth.models import User


class EventType(models.Model):
    type = models.CharField(max_length=255)

    def __repr__(self):
        return "EventType(type={})".format(self.type)

    def __str__(self):
        return str(self.type)


class Event(models.Model):
    name        = models.CharField(max_length=255)
    slug        = models.CharField(max_length=255)
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField()
    location    = models.CharField(max_length=255)
    event_type  = models.ForeignKey(EventType, models.CASCADE)
    description = models.TextField()
    rsvp_limit  = models.PositiveIntegerField(null=True, blank=True)
    # need_transportation = models.BooleanField(default=False)
    # view_permission_group_id = models.IntegerField(null=True)
    # rsvp_permission_group_id = models.IntegerField(null=True)
    # view_permission_group_id = models.ForeignKey('people.Group', on_delete=models.SET_NULL, null=True)
    # rsvp_permission_group_id = models.ForeignKey('people.Group', on_delete=models.SET_NULL, null=True)
    # markdown    = models.BooleanField(default=False)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at  = models.DateTimeField(auto_now_add=True)
    # updated_at  = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '/events/{}'.format(self.id)

    def __repr__(self):
        return "Event(name={}, location={})".format(self.name, self.location)

    def __str__(self):
        return self.name

    def admitted_set(self):
        return self.rsvp_set.order_by("created_at")[:self.rsvp_limit]

    def waitlist_set(self):
        if not self.rsvp_limit:
            return self.rsvp_set.none()
        return self.rsvp_set.order_by("created_at")[self.rsvp_limit:]


class Rsvp(models.Model):
    user  = models.ForeignKey(User, models.CASCADE, verbose_name="rsvp'd by")
    event = models.ForeignKey(Event, models.CASCADE)
    confirmed       = models.BooleanField(default=False)
    comment         = models.TextField(blank=True, default="")
    # transportation  = models.IntegerField(choices=TRANSPORT_ENUM,
    #                                       default=HAVE_RIDE)
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name="rsvp time")
    # updated_at      = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "Rsvp(user={}, event={})".format(self.user, self.event)

    def __str__(self):
        return "{} {} @ {}".format(self.user.first_name, self.user.last_name, self.event.name)

    def waitlisted(self):
        if self.event.rsvp_limit is None:
            return False
        rsvps_before_self = self.event.rsvp_set.filter(created_at__lt=self.created_at).count()
        return rsvps_before_self <= self.event.rsvp_limit

    def waitlist_position(self):
        if not self.waitlisted():
            return None
        return self.event.rsvp_set.filter(created_at__lt=self.created_at).count() \
                - self.event.rsvp_limit + 1
