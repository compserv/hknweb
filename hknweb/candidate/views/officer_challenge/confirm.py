from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from hknweb.utils import login_and_permission

from hknweb.candidate.forms import ChallengeConfirmationForm
from hknweb.candidate.models import OffChallenge
from hknweb.candidate.utils import send_challenge_confirm_email


@login_and_permission("candidate.change_offchallenge")
def officer_confirm_view(request, pk):
    """Officer views and confirms a challenge request after clicking email link.
    Only the officer who gave the challenge can review it."""
    challenge = OffChallenge.objects.get(id=pk)
    if request.user.id != challenge.officer.id:
        raise PermissionDenied  # not the officer that gave the challenge

    requester_name = challenge.requester.get_full_name()
    form = ChallengeConfirmationForm(request.POST or None, instance=challenge)
    context = {
        "challenge": challenge,
        "requester_name": requester_name,
        "form": form,
    }

    if form.is_valid():
        form.instance.reviewed = True
        form.save()
        # csec has already confirmed, and now officer confirms
        if challenge.officer_confirmed is True and challenge.csec_confirmed is True:
            send_challenge_confirm_email(request, form.instance, True)
        # csec has not already rejected, and now officer rejects
        elif (
            challenge.officer_confirmed is False
            and challenge.csec_confirmed is not False
        ):
            send_challenge_confirm_email(request, form.instance, False)
        # if neither is true, either need to wait for csec to review,
        # or csec has already rejected
        return redirect(
            "/cand/reviewconfirm/{}".format(pk)
        )  # lgtm [py/url-redirection]
    return render(request, "candidate/challenge_confirm.html", context=context)


@login_and_permission("candidate.change_offchallenge")
def confirm_challenge(request, id):
    if request.method != "POST":
        raise Http404()

    offchallenge = get_object_or_404(OffChallenge, id=id)
    offchallenge.officer_confirmed = True
    offchallenge.save()

    next_page = request.POST.get("next", "/")
    return redirect(next_page)  # lgtm [py/url-redirection]


@login_and_permission("candidate.view_offchallenge")
def officer_review_confirmation(request, pk):
    """The page displayed after officer reviews challenge and clicks "submit." """
    challenge = OffChallenge.objects.get(id=pk)
    requester_name = challenge.requester.get_full_name()
    context = {
        "challenge": challenge,
        "requester_name": requester_name,
    }
    return render(request, "candidate/review_confirm.html", context=context)
