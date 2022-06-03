from django.db.models import Q, QuerySet
from django.contrib.auth.models import User

from dal import autocomplete

from hknweb.utils import allow_public_access

from hknweb.coursesemester.models import Course
from hknweb.tutoring.models import TutoringLogistics


class CourseAutocomplete(autocomplete.Select2QuerySetView):  # pragma: no cover
    def get_queryset(self):
        courses = Course.objects
        if self.q:
            courses = courses.filter(
                Q(name__icontains=self.q)
                | Q(number__icontains=self.q)
                | Q(department__abbreviated_name__icontains=self.q)
                | Q(department__long_name__icontains=self.q)
            )
        return courses.order_by("number", "department__abbreviated_name")


def get_tutors() -> "QuerySet[User]":
    logistics = TutoringLogistics.get_most_recent()
    if logistics is None:
        return User.objects.none()

    return User.objects.filter(tutoring_slots__in=logistics.slot_set.all()).distinct()


class TutorAutocomplete(autocomplete.Select2QuerySetView):  # pragma: no cover
    def get_queryset(self):
        tutors = get_tutors()
        if self.q:
            tutors = tutors.filter(
                Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
            )
        return tutors.order_by("first_name", "last_name")


course_autocomplete = allow_public_access(CourseAutocomplete.as_view())
tutor_autocomplete = allow_public_access(TutorAutocomplete.as_view())
