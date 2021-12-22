from django.db import models

from hknweb.academics.models.base_models import AcademicEntity


class ICSR(AcademicEntity):
    """
    InstructorCourseSemesterRelation (ICSR)
    """

    # reference attributes
    icsr_course = models.ForeignKey(
        "Course", on_delete=models.PROTECT, related_name="icsr_course"
    )
    icsr_department = models.ForeignKey(
        "Department", on_delete=models.PROTECT, related_name="icsr_department"
    )
    icsr_instructor = models.ForeignKey(
        "Instructor", on_delete=models.PROTECT, related_name="icsr_instructor"
    )
    icsr_semester = models.ForeignKey(
        "Semester", on_delete=models.PROTECT, related_name="icsr_semester"
    )

    # value attributes
    first_name = models.TextField(max_length=100)
    last_name = models.TextField(max_length=100)
    course_number = models.TextField(max_length=100)
    section_type = models.TextField(max_length=100)
    section_number = models.TextField(max_length=100)
    instructor_type = models.TextField(max_length=100)
