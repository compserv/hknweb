from django.db import models
from django.db.models import Case, When, Value, Model

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
        from .logistics import Semester

        if self.pk is None:
            l = [Semester.SPRING, Semester.SUMMER, Semester.FALL]
            self_num_sem = l.index(self.icsr_semester.year_section) + 1
            latest_instructor_icsr = ICSR.recency_ordering(ICSR.objects.filter(
                icsr_instructor=self.icsr_instructor)).first()

            if self.icsr_semester.year > latest_instructor_icsr.icsr_semester.year or (
                    self.icsr_semester.year == latest_instructor_icsr.icsr_semester.year and
                    self_num_sem >= latest_instructor_icsr.numerical_semester):
                self.icsr_instructor.current_first_name = self.first_name
                self.icsr_instructor.current_last_name = self.last_name
                self.icsr.current_instructor_type = self.instructor_type

            latest_course_icsr = ICSR.recency_ordering(ICSR.objects.filter(
                icsr_course=self.icsr_course)).first()

            if self.icsr_semester.year > latest_course_icsr.icsr_semester.year or (
                    self.icsr_semester.year == latest_course_icsr.icsr_semester.year and
                    self_num_sem >= latest_course_icsr.numerical_semester):
                self.icsr_course.current_name = self.course_name
                self.icsr_instructor.current_number = self.course_number
        return super(AcademicEntity, self).save(*args, **kwargs)
