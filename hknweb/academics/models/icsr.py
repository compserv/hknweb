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
    def recency_ordering(qs):
        from .logistics import Semester
        return qs.annotate(numerical_semester=Case(
            When(icsr_semester__year_section=Semester.SPRING, then=Value(1)),
            When(icsr_semester__year_section=Semester.SUMMER, then=Value(2)),
            When(icsr_semester__year_section=Semester.FALL, then=Value(3)))).order_by \
            ("-icsr_semester__year", "-numerical_semester")

    def save(self, *args, **kwargs):
        this_semester = _chrono(self.icsr_semester)
        latest_instructor_sem = _chrono(self.icsr_instructor.recent_semester)

        if this_semester >= latest_instructor_sem:
            self.icsr_instructor.current_first_name = self.first_name
            self.icsr_instructor.current_last_name = self.last_name
            self.icsr_instructor.current_instructor_type = self.instructor_type
            self.icsr_instructor.recent_semester = this_semester
            self.icsr_instructor.save()
        latest_course_sem = _chrono(self.icsr_course.recent_semester)

        if this_semester >= latest_course_sem:
            self.icsr_course.current_name = self.course_name
            self.icsr_course.current_number = self.course_number
            self.icsr_course.recent_semester = this_semester
            self.icsr_course.save()
        return super(ICSR, self).save(*args, **kwargs)


"""
The purpose of this method is, given a semester, create a value that can be used to compare it to other semesters
chronologically
"""


def _chrono(semester):
    from .logistics import Semester
    if semester:
        l = [Semester.SPRING, Semester.SUMMER, Semester.FALL]
        return 3 * semester.year + l.index(semester.year_section)
    return 0
