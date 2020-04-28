from django.db import models

# Create your models here.

class Resume(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, blank=False)
    notes = models.TextField(max_length=1000, blank=True)
    document = models.FileField(upload_to='resume/', blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    critiques = models.TextField(max_length = 10000, blank=True)
