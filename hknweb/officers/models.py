from django.db import models

class Officer (models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 255)
    imange = models.CharField(max_length = 255, default = "")
    title = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    department = models.CharField(max_length = 255, default = "")
    personal_email = models.CharField(max_length = 255)
    def __str__(self):
        return "Officer(name = {} , title{}".format(self.name,self.title)


# class Event(models.Model):
#     id          = models.IntegerField(primary_key=True)
#     name        = models.CharField(max_length=255, null=False)
#     slug        = models.CharField(max_length=255)
#     location    = models.CharField(max_length=255)
#     description = models.TextField()
#     start_time  = models.DateTimeField(null=False)
#     end_time    = models.DateTimeField(null=False)
#     event_type_id = models.IntegerField()
#     # event_type_id  = models.ForeignKey()
#     need_transportation = models.BooleanField(default=False)
#     view_permission_group_id = models.IntegerField(null=True)
#     rsvp_permission_group_id = models.IntegerField(null=True)
#     # view_permission_group_id = models.ForeignKey('people.Group', on_delete=models.SET_NULL, null=True)
#     # rsvp_permission_group_id = models.ForeignKey('people.Group', on_delete=models.SET_NULL, null=True)
#     markdown    = models.BooleanField(default=False)
#     created_at  = models.DateTimeField(auto_now_add=True)
#     updated_at  = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return "Event(name={}, location={})".format(self.name, self.location)


# class Rsvp(models.Model):
#     NEED_RIDE = -1
#     HAVE_RIDE = 0
#     SM_SEDAN = 3
#     SEDAN = 4
#     MINIVAN = 6

#     TRANSPORT_ENUM = (
#         (NEED_RIDE, "I need a ride"),
#         (HAVE_RIDE, "Don't worry about me"),
#         (SM_SEDAN,  "I have a small sedan (4 seats)"),
#         (SEDAN,     "I have a sedan (5 seats)"),
#         (MINIVAN,   "I have a minivan (7 seats)"),
#     )

#     CONFIRMED = 't'
#     UNCONFIRMED = 'f'
#     REJECTED = 'r'

#     CONFIRMATION = (
#         (CONFIRMED,     "Confirmed"),
#         (UNCONFIRMED,   "Unconfirmed"),
#         (REJECTED,      "Rejected"),
#     )

#     id              = models.IntegerField(primary_key=True)
#     confirmed       = models.CharField(max_length=1,
#                                        choices=CONFIRMATION,
#                                        default=UNCONFIRMED)
#     confirm_comment = models.TextField()
#     person_id       = models.IntegerField(null=True)
#     # person_id       = models.ForeignKey('people.Person', on_delete=models.CASCADE)
#     event_id        = models.ForeignKey(Event, on_delete=models.CASCADE)
#     comment         = models.TextField()
#     transportation  = models.IntegerField(choices=TRANSPORT_ENUM,
#                                           default=HAVE_RIDE)
#     created_at      = models.DateTimeField(auto_now_add=True)
#     updated_at      = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return "RSVP(person_id={}, event_id={})".format(self.person, self.event)