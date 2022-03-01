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

from hknweb.candidate.forms import BitByteRequestForm
from hknweb.candidate.models import BitByteActivity


@method_login_and_permission("candidate.add_bitbyteactivity")
class BitByteView(FormView, generic.ListView):
    """Form for submitting bit-byte activity requests and list of past requests for candidate.
    Officers can still visit this page, but it will not have any new entries."""

    template_name = "candidate/bitbyte.html"
    form_class = BitByteRequestForm
    success_url = "/cand/bitbyte"

    context_object_name = "bitbyte_list"

    # resolve conflicting inheritance
    def get(self, request, *args, **kwargs):
        return generic.ListView.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        self.send_request_email(form)
        messages.success(self.request, "Your request was submitted to the VP!")
        return super().form_valid(form)

    def send_request_email(self, form):
        subject = "[HKN] Bit-byte request submitted"
        participant_emails = [part.email for part in form.instance.participants.all()]

        bitbyte_link = self.request.build_absolute_uri(reverse("candidate:bitbyte"))
        html_content = render_to_string(
            "candidate/bitbyte_request_email.html",
            {
                "subject": subject,
                "requester": self.request.user,
                "participants": form.instance.participants.all(),
                "bitbyte_link": bitbyte_link,
                "img_link": get_rand_photo(),
            },
        )
        msg = EmailMultiAlternatives(
            subject, subject, settings.NO_REPLY_EMAIL, participant_emails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_queryset(self):
        result = BitByteActivity.objects.filter(
            participants__exact=self.request.user
        ).order_by("-request_date")
        return result
