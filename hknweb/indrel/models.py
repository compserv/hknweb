from django.db import models

# Create your models here.
MAX_STRLEN = 100


class Resume(models.Model):
    #Name + Graduation Year
    first_name = models.CharField(max_length=MAX_STRLEN)
    last_name = models.CharField(max_length=MAX_STRLEN)
    middle_name = models.CharField(max_length=MAX_STRLEN, blank=True)
    grad_year = models.DateField()
    
    #If they are a current member and/or if this is the resume that should be included
    current = models.BooleanField()
    
    #Not Too sure about this one
    pdf = models.FileField(upload_to="resume/")
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Resume"
    
#class ResumeBook(models.Model):
    
    
    
