from django.db import models
from hknweb.models import Profile

max_strlen = 255 # default max length for char fields
max_txtlen = 2000 # default max length for text fields


# model for an officer challenge submitted by a candidate
class OffChallenge(models.Model):

    id              = models.AutoField(primary_key=True)
    officer         = models.ForeignKey('hknweb.Profile', on_delete=models.CASCADE)
    name            = models.CharField(max_length=max_strlen, default='')
    description     = models.TextField(max_length=max_txtlen, blank=True, default='')
    # proof of completion is optional (if proof is a file, the candiate can send it to slack)
    proof           = models.TextField(max_length=max_txtlen, blank=True, default='')

    # TODO not sure if I need a field for partners

    def __str__(self):
        return self.name
