from django import forms

from hknweb.exams.models import Course, Semester

EXAMS = [("midterm1", "Midterm 1"), ("midterm2", "Midterm 2"), ("final", "Final")]
TYPES = [("exam", "Exam"), ("sol", "Solution")]


class ExamUploadForm(forms.Form):

    course = forms.ModelChoiceField(queryset=Course.objects.all())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    exam = forms.CharField(label="Exam", widget=forms.Select(choices=EXAMS))
    type = forms.CharField(label="Type", widget=forms.Select(choices=TYPES))

    file = forms.FileField(label="Exam")
