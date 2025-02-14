from django.db import models

from hknweb.models import Profile

# Create your models here.
MAX_STRLEN = 100


class Resume(models.Model):
    # Name + Graduation Year
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, editable=False)

    # If they are a current member and/or if this is the resume that should be included
    current = models.BooleanField()

    # Resume PDF
    pdf = models.FileField(upload_to="resume/")


    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Resume"


# class ResumeBook(models.Model):
