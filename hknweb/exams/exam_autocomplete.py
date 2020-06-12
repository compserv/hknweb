# from dal import autocomplete

# from .models import Course, Department, Instructor, Semester, CourseSemester


# class CourseSemesterAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         allQs = CourseSemester.objects.all()
#         if self.q:
#             qs = allQs
#             searchTerms = self.q.split(" ")
#             checkedIndexes = set()
#             def lookup(qs, filterAction):
#                 for i in range(len(searchTerms)):
#                     if i in checkedIndexes:
#                         continue
#                     term = searchTerms[i]
#                     filteredQs = filterAction(qs, term)
#                     if filteredQs:
#                         qs = filteredQs
#                         checkedIndexes.add(i)
#                 return qs
#             qs = lookup(qs, lambda qs, term: qs.filter(semester__semester__contains=term))
#             qs = lookup(qs, lambda qs, term: qs.filter(course__department__abbreviated_name__contains=term))
#             qs = lookup(qs, lambda qs, term: qs.filter(course__number__contains=term))
#             if len(checkedIndexes) == 0:
#                 return CourseSemester.objects.none()
#             return qs
#         return allQs
    
#     def get_result_label(self, item):
#         return str(item.semester) + " " + str(item.course)

#     def get_selected_result_label(self, item):
#         return str(item.semester) + " " + str(item.course)
