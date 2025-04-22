from django.shortcuts import render
from hknweb.utils import login_and_access_level, GROUP_TO_ACCESSLEVEL


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def tutoringportal(request):
    return render(request, "tutoring/portal.html")
