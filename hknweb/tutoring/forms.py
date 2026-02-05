from django import forms

from dal import autocomplete

from hknweb.coursesemester.models import Course
from hknweb.studentservices.models import CourseDescription
from hknweb.tutoring.models import CribSheet
from hknweb.tutoring.views.autocomplete import get_tutors
from django.core.exceptions import ValidationError
import os


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


class AddCribForm(forms.Form):
    course = forms.ModelChoiceField(queryset=CourseDescription.objects.all())
    title = forms.CharField(max_length=100)
    comment = forms.CharField(max_length=300, required=False)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"accept": ".pdf"}))

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    ALLOWED_EXTENSIONS = {".pdf"}
    ALLOWED_MIME_TYPES = {"application/pdf"}

    def clean_file(self):
        file = self.cleaned_data["file"]

        if file.size > self.MAX_FILE_SIZE:
            raise ValidationError("File too large (max 5MB).")

        ext = os.path.splitext(file.name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise ValidationError("Unsupported file type.")

        if file.content_type not in self.ALLOWED_MIME_TYPES:
            raise ValidationError("Unsupported file type.")

        return file
