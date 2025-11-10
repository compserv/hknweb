from django.shortcuts import render
from hknweb.utils import login_and_committee
from hknweb.studentservices.models import CourseDescription
from hknweb.tutoring.forms import AddCourseForm
from django.conf import settings


@login_and_committee(settings.TUTORING_GROUP)
def courses(request):
    if request.method == "POST":
        new_course = AddCourseForm(request.POST)
        if new_course.is_valid():
            new_course.save()

    courses = [
        (course.title, course.updated_at, course.slug)
        for course in CourseDescription.objects.all().order_by("slug")
    ]
    form = AddCourseForm()

    context = {"courses": courses, "form": form}

    return render(request, "tutoring/courses.html", context=context)
