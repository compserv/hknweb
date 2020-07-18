from django.db import models
from django.core.validators import MinValueValidator

from .base_models import AcademicEntity


class Question(AcademicEntity):
    pass


class Survey(AcademicEntity):
    # reference attributes
    survey_icsr = models.ForeignKey('ICSR', on_delete=models.PROTECT, related_name='survey_icsr')

    # value attributes
    num_students = models.PositiveIntegerField()
    response_count = models.IntegerField(validators=[MinValueValidator(0)])
    is_private = models.BooleanField(default=True)


class Rating(AcademicEntity):
    # reference attributes
    rating_question = models.ForeignKey('Question', on_delete=models.PROTECT, related_name='rating_question')
    rating_survey = models.ForeignKey('Survey', on_delete=models.PROTECT, related_name='rating_survey')

    # value attributes
    question_text = models.TextField(max_length=500)
    inverted = models.BooleanField(default=False)
    range_max = models.IntegerField(default=7)
    rating_value = models.FloatField()
