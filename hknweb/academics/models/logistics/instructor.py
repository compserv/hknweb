from django.db import models

from hknweb.academics.models.base_models import AcademicEntity


class Instructor(AcademicEntity):
    instructor_id = models.CharField(max_length=255, primary_key=True)
