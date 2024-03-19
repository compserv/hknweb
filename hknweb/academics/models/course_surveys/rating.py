from django.db import models

from hknweb.academics.models.base_models import AcademicEntity


class Rating(AcademicEntity):
    # reference attributes
    rating_question = models.ForeignKey(
        "Question", on_delete=models.PROTECT, related_name="rating_question"
    )
    rating_survey = models.ForeignKey(
        "Survey", on_delete=models.PROTECT, related_name="rating_survey"
    )

    # value attributes
    question_text = models.TextField(max_length=2000)
    inverted = models.BooleanField(default=False)
    range_max = models.IntegerField(default=7)
    rating_value = models.FloatField()
