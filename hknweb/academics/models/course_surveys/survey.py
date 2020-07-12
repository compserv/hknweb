from django.db import models
from django.core.validators import MinValueValidator

from hknweb.academics.models.base_models import AcademicEntity


class Survey(AcademicEntity):
    # reference attributes
    survey_icsr = models.ForeignKey(
        "ICSR", on_delete=models.PROTECT, related_name="survey_icsr"
    )

    # value attributes
    num_students = models.PositiveIntegerField()
    response_count = models.IntegerField(validators=[MinValueValidator(0)])
    is_private = models.BooleanField(default=True)
