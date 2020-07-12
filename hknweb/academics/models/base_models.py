from django.db import models

class AcademicEntity(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
