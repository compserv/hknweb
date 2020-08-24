from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Count, Case, When, Value

from .base_models import AcademicEntity
from .icsr import ICSR


class Question(AcademicEntity):
    CHILDREN = ["rating"]
    @staticmethod
    def merge(primary, duplicates):
        if len(duplicates) == 0:
            raise Exception()
        affected_ratings = duplicates[0].rating_set
        for dup in duplicates[1:]:
            affected_ratings = affected_ratings | dup.rating_set
        errors = affected_ratings.values("rating_survey").annotate(count=Count("id")).filter(count__gt=1)

        if errors.exists():
            print("Merge Conflict Question. Rating ids: " + [x.id for x in errors])
            return
        affected_ratings.update(rating_question=primary)
    def get_current_question_text(self):
        return Rating.recency_ordering(self.rating_set).first().question_text
class Survey(AcademicEntity):
    # reference attributes
    survey_icsr = models.ForeignKey('ICSR', on_delete=models.PROTECT) # note this is a 1-1 relationship
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

    @staticmethod
    def recency_ordering(qs):
        from .logistics import Semester
        return qs.annotate(numerical_semester=Case(
            When(rating_survey__survey_icsr__icsr_semester__year_section=Semester.SPRING, then=Value(1)),
            When(rating_survey__survey_icsr__icsr_semester__year_section=Semester.SUMMER, then=Value(2)),
            When(rating_survey__survey_icsr__icsr_semester__year_section=Semester.FALL, then=Value(3)))).order_by \
            ("-rating_survey__survey_icsr__icsr_semester__year", "-numerical_semester")
