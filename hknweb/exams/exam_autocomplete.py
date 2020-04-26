from dal import autocomplete

from .models import Course, Department, Instructor, Semester, CourseSemester


class CourseSemesterAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return CourseSemester.objects.all()
    
    def get_result_label(self, item):
        return str(item.semester) + " " + str(item.course)

    def get_selected_result_label(self, item):
        return str(item.semester) + " " + str(item.course)
