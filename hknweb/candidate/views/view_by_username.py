from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from hknweb.utils import (
    GROUP_TO_ACCESSLEVEL,
    login_and_access_level,
)


@login_and_access_level(GROUP_TO_ACCESSLEVEL["member"])
def candidate_portal_view_by_username(request, username):
    user = User.objects.filter(username=username).first()
    if user is None:
        messages.warning(request, "User {} does not exist.".format(username))
        return HttpResponseRedirect(reverse("candidate:index"))

    user_cand_data = {}
    user_cand_data["user_self"] = False
    return render(request, "candidate/index.html", context=user_cand_data)
