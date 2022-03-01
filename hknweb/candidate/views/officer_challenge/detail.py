from django.shortcuts import render, reverse
from django.urls import reverse

from hknweb.utils import login_and_permission

from hknweb.candidate.models import OffChallenge


@login_and_permission("candidate.view_offchallenge")
def challenge_detail_view(request, pk):
    """Detail view of an officer challenge."""
    challenge = OffChallenge.objects.get(id=pk)
    officer_name = challenge.officer.get_full_name()
    requester_name = challenge.requester.get_full_name()

    # check whether the viewer of page is the officer who gave the challenge
    viewer_is_the_officer = challenge.officer == request.user
    # check whether the viewer of page is an officer
    if viewer_is_the_officer:
        review_link = request.build_absolute_uri(
            reverse("candidate:challengeconfirm", kwargs={"pk": pk})
        )
    else:
        review_link = None
    context = {
        "challenge": challenge,
        "officer_name": officer_name,
        "requester_name": requester_name,
        "viewer_is_the_officer": viewer_is_the_officer,
        # viewer_is_an_officer is already added as a context variable with a context processor
        "review_link": review_link,
    }
    return render(request, "candidate/challenge_detail.html", context=context)
