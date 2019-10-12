from django.db import models
from django.contrib.auth.models import User


class EventType(models.Model):
    type = models.CharField(max_length=255)

    def __repr__(self):
        return "EventType(type={})".format(self.type)

    def __str__(self):
        return str(self.type)


class Event(models.Model):
    name        = models.CharField(max_length=255, null=False)
    slug        = models.CharField(max_length=255)
    start_time  = models.DateTimeField(null=False)
    end_time    = models.DateTimeField(null=False)
    location    = models.CharField(max_length=255)
    event_type  = models.ForeignKey(EventType, models.CASCADE, null=False)
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


class Rsvp(models.Model): # TODO: null should be false in some cases
    user  = models.ForeignKey(User, models.CASCADE, null=False, verbose_name="rsvp'd by")
    event = models.ForeignKey(Event, models.CASCADE, null=False)
    confirmed       = models.BooleanField(null=False, default=False)
    comment         = models.TextField(blank=True, default="")
    # transportation  = models.IntegerField(choices=TRANSPORT_ENUM,
    #                                       default=HAVE_RIDE)
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name="rsvp time")
    # updated_at      = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "Rsvp(event={})".format(self.event)
    
    def __str__(self):
        return self.event.name
