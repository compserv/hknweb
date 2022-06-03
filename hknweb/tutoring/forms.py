from django import forms

from dal import autocomplete

from hknweb.coursesemester.models import Course


class CourseFilterForm(forms.Form):
    course = forms.ModelMultipleChoiceField(
        Course.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="tutoring:autocomplete_course",
            attrs={
                "name": "bob",
                "onchange": "course_selector_decorator()",
            },
        ),
    )
