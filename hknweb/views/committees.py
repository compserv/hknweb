from hknweb.utils import allow_public_access
from django.shortcuts import render
from hknweb.utils import login_and_access_level, GROUP_TO_ACCESSLEVEL


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def portal(request):
    return render(request, "committees.html")
