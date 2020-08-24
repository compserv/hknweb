from django.db import models
from django.db.models import Case, When, Value

from .base_models import AcademicEntity



class ICSR(AcademicEntity):
    """
    InstructorCourseSemesterRelation (ICSR)
    """
    # reference attributes
    icsr_course = models.ForeignKey('Course', on_delete=models.PROTECT)
    icsr_department = models.ForeignKey('Department', on_delete=models.PROTECT)
    icsr_instructor = models.ForeignKey('Instructor', on_delete=models.PROTECT)
    icsr_semester = models.ForeignKey('Semester', on_delete=models.PROTECT)

    # value attributes
    first_name = models.TextField(max_length=100)
    last_name = models.TextField(max_length=100)
    course_number = models.TextField(max_length=100)
    course_name = models.TextField(max_length=200)
    section_type = models.TextField(max_length=100)
    section_number = models.TextField(max_length=100)
    instructor_type = models.TextField(max_length=100)

    @staticmethod
    def merge(primary, duplicates):
        if len(duplicates) == 0:
            raise Exception()
        affected_surveys = duplicates[0].rating_question
        for dup in duplicates[1:]:
            affected_surveys = affected_surveys | dup.rating_question
        errors = affected_surveys.values("rating_survey").annotate(count=Count("id")).filter(count__gt=1)

        if errors.exists():
            print("Merge Conflict Question. Rating ids: " + [x.id for x in errors])
            return
        affected_surveys.update(rating_question=primary)
    @staticmethod
    def recency_ordering(qs):
        from .logistics import Semester
        return qs.annotate(numerical_semester=Case(
            When(icsr_semester__year_section=Semester.SPRING, then=Value(1)),
            When(icsr_semester__year_section=Semester.SUMMER, then=Value(2)),
            When(icsr_semester__year_section=Semester.FALL, then=Value(3)))).order_by \
            ("-icsr_semester__year", "-numerical_semester")





