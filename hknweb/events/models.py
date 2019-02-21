from django.db import models
from hknweb.models import Profile

class Event(models.Model):
    name        = models.CharField(max_length=255, null=False)
    slug        = models.CharField(max_length=255)
    location    = models.CharField(max_length=255)
    description = models.TextField()
    start_time  = models.DateTimeField(null=False)
    end_time    = models.DateTimeField(null=False)
    rsvp_limit  = models.PositiveIntegerField(null=True, default=999999) # I'm being rather pessimistic in assuming no HKN event will hit 1 million participants!
    rsvps       = models.IntegerField(default=0)
    # event_type_id = models.IntegerField()
    # event_type_id  = models.ForeignKey()
    # need_transportation = models.BooleanField(default=False)
    # view_permission_group_id = models.IntegerField(null=True)
    # rsvp_permission_group_id = models.IntegerField(null=True)
    # view_permission_group_id = models.ForeignKey('people.Group', on_delete=models.SET_NULL, null=True)
    # rsvp_permission_group_id = models.ForeignKey('people.Group', on_delete=models.SET_NULL, null=True)
    # markdown    = models.BooleanField(default=False)
    # created_at  = models.DateTimeField(auto_now_add=True)
    # updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Event(name={}, location={})".format(self.name, self.location)


class Rsvp(models.Model):
    # CONFIRMED = 't'
    # UNCONFIRMED = 'f'
    # REJECTED = 'r'

    # CONFIRMATION = (
    #     (CONFIRMED,     "Confirmed"),
    #     (UNCONFIRMED,   "Unconfirmed"),
    #     (REJECTED,      "Rejected"),
    # )

    # user  = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # id    = models.IntegerField(primary_key=True)
    # confirmed       = models.CharField(max_length=1,
    #                                    choices=CONFIRMATION,
    #                                    default=UNCONFIRMED)
    # confirm_comment = models.TextField()
    # comment         = models.TextField()
    # transportation  = models.IntegerField(choices=TRANSPORT_ENUM,
    #                                       default=HAVE_RIDE)
    # created_at      = models.DateTimeField(auto_now_add=True)
    # updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "RSVP(event={})".format(self.event)