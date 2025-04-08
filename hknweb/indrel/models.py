from django.db import models

from hknweb.models import Profile

# Create your models here.
MAX_STRLEN = 100


class UserResume(models.Model):
    # Name + Graduation Year
    userInfo = models.OneToOneField(Profile, on_delete=models.CASCADE, editable=True, related_name="resume")

    resume = models.FileField(upload_to="indrel/resume/", null=True, blank=True)
    
    upload_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.userInfo.user.last_name}, {self.userInfo.user.first_name}"


class ResumeBook(models.Model):
    pdf = models.FileField(upload_to="indrel/resumebooks/")
    
    iso = models.FileField(upload_to="indrel/resumebooks/")
    
    comments = models.CharField(max_length=500, blank=True)
    
    creation_date = models.DateTimeField(auto_now_add=True)
    