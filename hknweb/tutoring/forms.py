from django import forms

from dal import autocomplete

from hknweb.coursesemester.models import Course
from hknweb.studentservices.models import CourseDescription
from hknweb.tutoring.models import CribSheet
from hknweb.tutoring.views.autocomplete import get_tutors


class CourseFilterForm(forms.Form):
    course = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=autocomplete.ModelSelect2Multiple(
            url="tutoring:autocomplete_course",
            attrs={"onchange": "selector_decorator()"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.all()


class TutorFilterForm(forms.Form):
    tutor = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=autocomplete.ModelSelect2Multiple(
            url="tutoring:autocomplete_tutor",
            attrs={"onchange": "selector_decorator()"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tutor"].queryset = get_tutors()


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = CourseDescription
        fields = ["title", "slug"]


class AddCribForm(forms.ModelForm):
    class Meta:
        model = CribSheet
        fields = ["course", "pdf", "comment"]
