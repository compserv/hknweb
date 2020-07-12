from django.db import models

from .base_models import AcademicEntity

from .icsr import ICSR


class Question(AcademicEntity):
    pass


class Survey(AcademicEntity):
    # reference attributes
    icsr = models.ForeignKey(ICSR, on_delete=models.CASCADE)

    # value attributes
    num_students = models.IntegerField()
    response_count = models.IntegerField()
    is_private = models.BooleanField(default=True)


class Rating(AcademicEntity):
    # reference attributes
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    # value attributes
    question_text = models.TextField(max_length=500)
    inverted = models.BooleanField(default=False)
    range_max = models.IntegerField(default=7)
    rating = models.FloatField()
