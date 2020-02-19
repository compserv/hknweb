from django.db import models

class Link(models.Model):
    name = models.CharField(max_length=255, null=False)
    redirect = models.URLField()
    leader = models.CharField(max_length=255, null=False)

