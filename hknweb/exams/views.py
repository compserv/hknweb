from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render

from hknweb.exams.forms import ExamUploadForm
from .models import Course, CourseSemester, Department, Instructor, Semester


def index(request):
    courses = Course.objects.order_by("name")
    departments = Department.objects.order_by("long_name")

    context = {
        "courses": courses,
        "searchCourses": CourseSemester.objects.all(),
        "departments": departments,
    }

    return render(request, "exams/index.html", context)


def exams_for_course(request, department, number):

    specificSemester = request.GET.get("term", "")

    department = Department.objects.get(abbreviated_name=department)
    course = Course.objects.filter(department__exact=department.id).get(
        number__exact=number
    )
    semesters = CourseSemester.objects.filter(course__exact=course.id)

    if specificSemester:
        subSemesters = semesters.filter(semester__semester__exact=specificSemester)
        if subSemesters:
            semesters = subSemesters
        else:
            specificSemester = ""

    context = {
        "course": course,
        "semesters": semesters,
        "selectedTerm": specificSemester,
    }

    return render(request, "exams/exams-course.html", context)


@permission_required("exams.add_coursesemester", login_url="/accounts/login/")
def add_exam(request):
    if request.method == "POST":
        form = ExamUploadForm(request.POST, request.FILES)
        if form.is_valid():
            semester = form.cleaned_data["semester"]
            course = form.cleaned_data["course"]
            exam = form.cleaned_data["exam"]
            type = form.cleaned_data["type"]

            courseSemester = CourseSemester.objects.filter(
                course=course, semester=semester
            )

            examName = exam + ("_sol" if (type == "sol") else "")

            if courseSemester.count != 1:
                return HttpResponseBadRequest(
                    (
                        "File {0} as {1} has been uploaded before already. "
                        + "Please press the Back button on your browser to return to the form."
                    ).format(request.FILES["file"], examName),
                    status=409,
                )

            courseSemester = courseSemester.first()

            setattr(courseSemester, examName, request.FILES["file"])
            courseSemester.save()

            return HttpResponseRedirect("/")
        else:
            return HttpResponseBadRequest(
                "An error has occured: {0}".format(form.errors), status=400
            )

    return render(request, "exams/exams_add.html", {"form": ExamUploadForm(None)})
