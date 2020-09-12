from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Case, When, Value

from .base_models import AcademicEntity
from .icsr import _chrono


class Question(AcademicEntity):
    recent_semester = models.ForeignKey("Semester", on_delete=models.PROTECT, blank=True, null=True)
    current_text = models.TextField(blank=True, null=True)
    CHILDREN = ["rating"]


class Survey(AcademicEntity):
    # reference attributes
    survey_icsr = models.ForeignKey('ICSR', on_delete=models.PROTECT)  # note this is a 1-1 relationship
    CHILDREN = ["rating"]
    # value attributes
    num_students = models.PositiveIntegerField()
    response_count = models.IntegerField(validators=[MinValueValidator(0)])
    is_private = models.BooleanField(default=True)


class Rating(AcademicEntity):
    # reference attributes
    rating_question = models.ForeignKey('Question', on_delete=models.PROTECT)
    rating_survey = models.ForeignKey('Survey', on_delete=models.PROTECT)

    # value attributes
    question_text = models.TextField(max_length=500)
    inverted = models.BooleanField(default=False)
    range_max = models.IntegerField(default=7)
    rating_value = models.FloatField()

    def save(self, *args, **kwargs):
        this_semester = _chrono(self.rating_survey.survey_icsr.icsr_semester)
        latest_text_sem = _chrono(self.rating_question.recent_semester)

        if this_semester >= latest_text_sem:
            self.rating_question.current_text = self.question_text
            self.rating_question.save()
        return super(Rating, self).save(*args, **kwargs)

    @staticmethod
    def recency_ordering(qs):
        from .logistics import Semester
        return qs.annotate(numerical_semester=Case(
            When(rating_survey__survey_icsr__icsr_semester__year_section=Semester.SPRING, then=Value(1)),
            When(rating_survey__survey_icsr__icsr_semester__year_section=Semester.SUMMER, then=Value(2)),
            When(rating_survey__survey_icsr__icsr_semester__year_section=Semester.FALL, then=Value(3)))).order_by \
            ("-rating_survey__survey_icsr__icsr_semester__year", "-numerical_semester")