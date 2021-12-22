from django.db import models

from hknweb.academics.models.base_models import AcademicEntity


class Department(AcademicEntity):
    name = models.TextField(max_length=200)
    abbr = models.TextField(max_length=100)
