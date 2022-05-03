from django.shortcuts import render

from hknweb.utils import (
    GROUP_TO_ACCESSLEVEL,
    login_and_access_level,
)


@login_and_access_level(GROUP_TO_ACCESSLEVEL["candidate"])
def candidate_portal(request):
    context = {}
    return render(request, "candidate/candidate_portal.html", context=context)
