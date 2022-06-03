from django.db.models import Q

from dal import autocomplete

from hknweb.utils import allow_public_access

from hknweb.coursesemester.models import Course


class CourseAutocomplete(autocomplete.Select2QuerySetView):
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


course_autocomplete = allow_public_access(CourseAutocomplete.as_view())
