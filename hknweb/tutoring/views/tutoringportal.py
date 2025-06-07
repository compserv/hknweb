from django.shortcuts import render
from hknweb.utils import login_and_committee, GROUP_TO_ACCESSLEVEL
from django.conf import settings


@login_and_committee(settings.TUTORING_GROUP)
def tutoringportal(request):
    return render(request, "tutoring/portal.html")
