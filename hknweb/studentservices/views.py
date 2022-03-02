import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views import generic
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from hknweb.utils import login_and_permission, method_login_and_permission

from hknweb.studentservices.models import DepTour, ReviewSession
from hknweb.studentservices.forms import (
    DocumentForm,
    ReviewSessionForm,
    ReviewSessionUpdateForm,
    TourRequest,
)


SUBMIT_TEMPLATE = "studentservices/resume_critique_submit.html"
UPLOADED_TEMPLATE = "studentservices/resume_critique_uploaded.html"


def resume_critique_submit(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, UPLOADED_TEMPLATE)
        else:
            form = DocumentForm()
            return render(
                request,
                SUBMIT_TEMPLATE,
                {
                    "form": form,
                    "err": True,
                },
            )

    form = DocumentForm()
    return render(
        request,
        SUBMIT_TEMPLATE,
        {
            "form": form,
            "err": False,
        },
    )


def resume_critique_uploaded(request):
    form = DocumentForm()
    return render(request, SUBMIT_TEMPLATE, {"form": form})


def reviewsessions(request):
    reviewsessions = ReviewSession.objects.order_by("-start_time")

    context = {
        "reviewsessions": reviewsessions,
    }
    return render(request, "studentservices/reviewsessions.html", context)


@login_and_permission("studentservices.view_reviewsession")
def reviewsession_details(request, id):
    reviewsession = get_object_or_404(ReviewSession, pk=id)

    context = {
        "reviewsession": reviewsession,
        "can_edit": request.user.has_perm("studentservices.change_review_session"),
    }
    return render(request, "studentservices/reviewsession_details.html", context)


@login_and_permission("studentservices.add_reviewsession")
def add_reviewsession(request):
    form = ReviewSessionForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            reviewsession = form.save(commit=False)
            reviewsession.created_by = request.user
            reviewsession.save()
            messages.success(request, "Review session has been added!")
            return redirect("studentservices:reviewsessions")
        else:
            messages.error(request, "Something went wrong oops")
            return render(
                request,
                "studentservices/reviewsession_add.html",
                {"form": ReviewSessionForm(None)},
            )
    return render(
        request,
        "studentservices/reviewsession_add.html",
        {"form": ReviewSessionForm(None)},
    )


@method_login_and_permission("reviewsession_add.change_review_session")
class ReviewSessionUpdateView(generic.edit.UpdateView):
    model = ReviewSession
    form_class = ReviewSessionUpdateForm
    template_name_suffix = "_edit"


def tours(request):
    tour = DepTour.objects

    context = {
        "tour": tour,
    }
    return render(request, "studentservices/tours.html", context)


def send_request_email(request, form):
    subject = "Department Tour Request"
    officer_email = "deprel@hkn.eecs.berkeley.edu"

    html_content = render_to_string(
        "studentservices/tour_request_email.html",
        {
            "name": form.instance.name,
            "time": form.instance.desired_time,
            "date": form.instance.date,
            "email": form.instance.email,
            "phone": form.instance.phone,
            "comments": form.instance.comments,
        },
    )
    msg = EmailMessage(
        subject, html_content, "no-reply@hkn.eecs.berkeley.edu", [officer_email]
    )
    msg.content_subtype = "html"
    msg.send()


def tour(request):
    form = TourRequest(request.POST or None)
    if request.method == "POST":

        if form.is_valid():
            tour = form.save(commit=False)
            tour.save()

            # send_request_email(request, form)

            messages.success(request, "Your request has been sent!")
            return redirect("studentservices:tours")
        else:
            msg = "Something went wrong! Your request did not send. Try again, or email deprel@hkn.mu."
            messages.error(request, msg)
    return render(request, "studentservices/tours.html", {"form": form})


def course_guide(request):
    return render(request, "studentservices/course_guide.html")


def course_guide_data(request):
    data = json.load(open("hknweb/studentservices/templates/studentservices/course_guide_data.json"))
    return JsonResponse(data)
