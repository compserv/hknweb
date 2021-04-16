from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    class Meta:
        verbose_name_plural = "Links"  # fix plural without using Meta class
    name = models.CharField(max_length=255, null=False, unique=True)
    redirect = models.URLField()
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    #    return "{} created by {}".format(self.name, self.creator)
