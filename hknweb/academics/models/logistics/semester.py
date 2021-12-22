from django.db import models
from django.core.validators import MinValueValidator

from hknweb.academics.models.base_models import AcademicEntity


class Semester(AcademicEntity):
    SPRING = "Sp"
    SUMMER = "Su"
    FALL = "Fa"
    YEAR_SECTION_CHOICES = [
        (SPRING, "Spring"),
        (SUMMER, "Summer"),
        (FALL, "Fall"),
    ]

    # !TODO Add validation for year and year_section.
    # See https://github.com/compserv/hknweb/commit/c619844de3efbab01cd63442157ad7d6303538ee
    year = models.IntegerField(validators=[MinValueValidator(1915)])
    year_section = models.TextField(max_length=100, choices=YEAR_SECTION_CHOICES)
