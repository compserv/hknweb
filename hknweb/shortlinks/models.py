from django.db import models

class Links(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    redirect = models.URLField()
    leader = models.CharField(max_length=255, null=False)

