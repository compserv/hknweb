from django.db import models

class Links(models.Model):
    class Meta:
        verbose_name_plural = "Links" #fix plural without using Meta class
    name = models.CharField(max_length=255, null=False, unique=True)
    redirect = models.URLField()
    leader = models.CharField(max_length=255, null=False)

