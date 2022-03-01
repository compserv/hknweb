from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView

from hknweb.utils import (
    get_rand_photo,
    method_login_and_permission,
)

from hknweb.candidate.forms import ChallengeRequestForm
from hknweb.candidate.models import OffChallenge


@method_login_and_permission("candidate.add_offchallenge")
class CandRequestView(FormView, generic.ListView):
    """Form for submitting officer challenge requests and list of past requests for candidate."""

    template_name = "candidate/candreq.html"
    form_class = ChallengeRequestForm
    success_url = "/cand/candreq"

    context_object_name = "challenge_list"

    # resolve conflicting inheritance
    def get(self, request, *args, **kwargs):
        return generic.ListView.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.requester = self.request.user
        form.save()
        self.send_request_email(form)
        messages.success(self.request, "Your request was submitted to the officer!")
        return super().form_valid(form)

    def send_request_email(self, form):
        subject = "[HKN] Confirm Officer Challenge"
        officer_email = form.instance.officer.email

        confirm_link = self.request.build_absolute_uri(
            reverse("candidate:challengeconfirm", kwargs={"pk": form.instance.id})
        )
        html_content = render_to_string(
            "candidate/challenge_request_email.html",
            {
                "subject": subject,
                "candidate_name": form.instance.requester.get_full_name(),
                "candidate_username": form.instance.requester.username,
                "confirm_link": confirm_link,
                "img_link": get_rand_photo(),
            },
        )
        msg = EmailMultiAlternatives(
            subject, subject, settings.NO_REPLY_EMAIL, [officer_email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_queryset(self):
        result = OffChallenge.objects.filter(
            requester__exact=self.request.user
        ).order_by("-request_date")
        return result
