from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from hknweb.utils import login_and_access_level, GROUP_TO_ACCESSLEVEL

from hknweb.candidate.models import OffChallenge, BitByteActivity


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def confirm_challenge(request, pk: int, action: int):
    if request.method != "POST":
        raise Http404()

    offchallenge = get_object_or_404(OffChallenge, pk=pk)
    offchallenge.officer_confirmed = action == 0  # 0 means confirmed
    offchallenge.save()

    return redirect("candidate:officer_portal")


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def confirm_bitbyte(request, pk: int, action: int):
    if request.method != "POST":
        raise Http404()

    bitbyte = get_object_or_404(BitByteActivity, pk=pk)
    bitbyte.confirmed = action == 0
    bitbyte.save()

    return redirect("candidate:officer_portal")
