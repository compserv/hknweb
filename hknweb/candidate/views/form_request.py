from django.http import Http404, HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import redirect

from hknweb.utils import login_and_access_level, GROUP_TO_ACCESSLEVEL

from hknweb.candidate.forms import BitByteRequestForm, ChallengeRequestForm


def form_request(request, form_cls, title: str):
    if request.method != "POST":
        return Http404()

    form = form_cls(request.POST or None)
    if not form.is_valid():
        return HttpResponseBadRequest()

    form.save()
    messages.success(request, f"Your {title} request was submitted!")
    return redirect("candidate:candidate_portal")


@login_and_access_level(GROUP_TO_ACCESSLEVEL["candidate"])
def bitbyte(request):
    return form_request(request, BitByteRequestForm, "bitbyte")


@login_and_access_level(GROUP_TO_ACCESSLEVEL["candidate"])
def officer_challenge_request(request):
    def form_wrapper(*args, **kwargs):
        form = ChallengeRequestForm(*args, **kwargs)
        form.instance.requester = request.user
        return form

    return form_request(request, form_wrapper, "officer challenge")
