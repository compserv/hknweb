from django.db import models
from django.contrib.auth.models import User

class ReviewSession(models.Model):
    name        = models.CharField(max_length=255)
    slug        = models.CharField(max_length=255)
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField()
    location    = models.CharField(max_length=255)
    description = models.TextField()

    created_by  = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at  = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return '/reviewsessions/{}'.format(self.id)

    def __repr__(self):
        return "Event(name={}, location={})".format(self.name, self.location)

    def __str__(self):
        return self.name
