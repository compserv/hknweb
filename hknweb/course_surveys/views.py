from django.shortcuts import render


def index(request):
    return render(request, "course_surveys/index.html")
