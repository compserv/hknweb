from django.db import models

from .base_models import AcademicEntity


class Course(AcademicEntity):
    pass


class Department(AcademicEntity):
    name = models.TextField(max_length=200)
    abbr = models.TextField(max_length=100)


class Instructor(AcademicEntity):
    instructor_id = models.TextField(max_length=500)


class Semester(AcademicEntity):
    SPRING = 'Sp'
    SUMMER = 'Su'
    FALL = 'Fa'
    YEAR_SECTION_CHOICES = [
        (SPRING, 'Spring'),
        (SUMMER, 'Summer'),
        (FALL, 'Fall'),
    ]

    year = models.TextField(max_length=100)
    year_section = models.TextField(max_length=100, choices=YEAR_SECTION_CHOICES)
