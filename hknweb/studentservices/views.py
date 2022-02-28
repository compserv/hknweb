from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import generic

from hknweb.utils import login_and_permission, method_login_and_permission
from hknweb.studentservices.models import ReviewSession
from hknweb.studentservices.forms import DocumentForm, ReviewSessionForm, ReviewSessionUpdateForm


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
