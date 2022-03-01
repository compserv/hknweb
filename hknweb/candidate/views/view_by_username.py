from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse

from hknweb.utils import (
    get_access_level,
    GROUP_TO_ACCESSLEVEL,
)

from hknweb.candidate.utils_candportal import CandidatePortalData


@login_required
def candidate_portal_view_by_username(request, username):
    if GROUP_TO_ACCESSLEVEL["member"] < get_access_level(request.user):
        messages.warning(request, "Insufficent permission to access a user.")
        return HttpResponseRedirect("/")
    
    user = User.objects.filter(username=username).first()
    if user is None:
        messages.warning(request, "User {} does not exist.".format(username))
        return HttpResponseRedirect(reverse("candidate:index"))
    cand_data = CandidatePortalData(user)
    user_cand_data = cand_data.get_user_cand_data()
    user_cand_data["user_self"] = False
    return render(request, "candidate/index.html", context=user_cand_data)
