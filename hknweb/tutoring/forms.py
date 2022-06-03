from django import forms

from dal import autocomplete

from hknweb.coursesemester.models import Course
from hknweb.tutoring.views.autocomplete import get_tutors


class CourseFilterForm(forms.Form):
    course = forms.ModelMultipleChoiceField(
        Course.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="tutoring:autocomplete_course",
            attrs={"onchange": "selector_decorator()"},
        ),
    )


class TutorFilterForm(forms.Form):
    tutor = forms.ModelMultipleChoiceField(
        get_tutors(),
        widget=autocomplete.ModelSelect2Multiple(
            url="tutoring:autocomplete_tutor",
            attrs={"onchange": "selector_decorator()"},
        ),
    )
