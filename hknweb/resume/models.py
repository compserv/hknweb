from django.db import models

# Create your models here.

class Resume(models.Model):
    name = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='resume/')
    uploaded_at = models.DateTimeField(auto_now_add=True)