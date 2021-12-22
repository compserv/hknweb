from django.shortcuts import render
from django.http import HttpResponse

from .models import Course

# Create your views here.
def index(request):
    courses = Course.objects.all()
    return render(request, "login.html", {"Courses": courses})


def courses(request, department, course_number):
    course = Course.objects.get(department=department, course_number=course_number)
    return render(request, "content.html", {"Courses": course})


def addCourse(request):
    return render(request, "addCourse.html")
