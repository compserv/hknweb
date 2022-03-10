from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import reverse
from django.template.loader import render_to_string

from hknweb.utils import get_rand_photo


def send_challenge_confirm_email(request, challenge, confirmed):
    subject = "[HKN] Your officer challenge was reviewed"
    candidate_email = challenge.requester.email

    challenge_link = request.build_absolute_uri(
        reverse("candidate:detail", kwargs={"pk": challenge.id})
    )
    html_content = render_to_string(
        "candidate/challenge_confirm_email.html",
        {
            "subject": subject,
            "confirmed": confirmed,
            "officer_name": challenge.officer.get_full_name(),
            "officer_username": challenge.officer.username,
            "challenge_link": challenge_link,
            "img_link": get_rand_photo(),
        },
    )
    msg = EmailMultiAlternatives(
        subject, subject, settings.NO_REPLY_EMAIL, [candidate_email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
