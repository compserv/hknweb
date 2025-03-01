from django.db import models

from hknweb.models import Profile

# Create your models here.
MAX_STRLEN = 100


class UserResume(models.Model):
    # Name + Graduation Year
    userInfo = models.OneToOneField(Profile, on_delete=models.CASCADE, editable=True)

    # If they are a current member and/or if this is the resume that should be included
    current = models.BooleanField()

    # Not Too sure about this one
    pdf = models.FileField(upload_to="resume/")
    
    def __str__(self):
        return f"{self.userInfo.user.last_name}, {self.userInfo.user.first_name}"



#class ResumeBook(models.Model):
