from django.db import models
from django.core.validators import MinValueValidator


from .base_models import AcademicEntity



class Course(AcademicEntity):
    CHILDREN = ["icsr"]
    current_name = models.TextField()
    current_number = models.TextField()


class Department(AcademicEntity):
    name = models.TextField(max_length=200)
    abbr = models.TextField(max_length=100)


class Instructor(AcademicEntity):
    instructor_id = models.TextField(max_length=500)
    current_first_name = models.TextField()
    current_last_name = models.TextField()
    current_instructor_type = models.TextField()
    CHILDREN = ["icsr"]


class Semester(AcademicEntity):
    SPRING = 'Sp'
    SUMMER = 'Su'
    FALL = 'Fa'
    YEAR_SECTION_CHOICES = [
        (SPRING, 'Spring'),
        (SUMMER, 'Summer'),
        (FALL, 'Fall'),
    ]

    # !TODO Add validation for year and year_section.
    # See https://github.com/compserv/hknweb/commit/c619844de3efbab01cd63442157ad7d6303538ee
    year = models.IntegerField(validators=[MinValueValidator(1915)])
    year_section = models.TextField(max_length=100, choices=YEAR_SECTION_CHOICES)
