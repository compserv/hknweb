from django.db import models


class EventType(models.Model):
    type = models.CharField(max_length=255)
    # Default color: CS61A blue
    color = models.CharField(max_length=7, default="#0072c1")

    def __repr__(self):
        return "EventType(type={})".format(self.type)

    def __str__(self):
        return str(self.type)
