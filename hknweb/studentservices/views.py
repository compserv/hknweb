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
    graph = {
        "16A": ["16B"],
        "16B": ["70", "Circuits", "Devices", "Signals/Control", "AI/ML", "Theory"],
        "70": ["Signals/Control", "AI/ML", "Theory"],
        "53": ["Signals/Control", "AI/ML"],
        "61A": ["61B"],
        "61B": ["61C", "AI/ML", "Theory", "Graphics", "Design"],
        "61C": ["Architecture", "Systems"],
        "Circuits": ["151", "105"],
        "105": ["140", "142", "113", "130"],
        "Devices": ["130", "117"],
        "130": ["134", "143"],
        "134": ["137A"],
        "113": ["137A"],
        "Signals/Control": ["127", "106A", "120", "128"],
        "106A": ["106B"],
        "106B": ["287"],
        "120": ["226A", "123", "221A", "229A", "128"],
        "123": ["145"],
        "128": ["221A", "192"],
        "AI/ML": ["126", "127"],
        "126": ["229A", "281A", "188", "189"],
        "127": ["189", "227B", "227C"],
        "188": ["189", "288"],
        "189": ["281A", "280", "182"],
        "281A": ["288", "281B"],
        "227B": ["227C"],
        "Theory": ["127", "170", "Math 113"],
        "170": ["172", "191", "174", "270", "271", "176"],
        "191": ["294"],
        "Graphics": ["184", "194-26"],
        "184": ["284B"],
        "Design": ["160", "169"],
        "160": ["260B"],
        "Architecture": ["151", "152"],
        "Systems": ["267", "164", "149", "168", "162", "186"],
        "164": ["264"],
        "168": ["268", "261N", "122", "161"],
        "122": ["261N"],
        "161": ["261", "194-35"],
        "261": ["261N"],
        "162": ["262A"],
        "262A": ["262B"],
    }

    groups = [
        ["16A", "16B", "70", "53", "61A", "61B", "61C"],
        ["Circuits", "151", "105", "140", "142"],
        ["Devices", "130", "117", "134", "143", "137A", "113"],
        ["Signals/Control", "127", "106A", "120", "128", "106B", "287", "226A", "123", "221A", "229A", "145", "192"],
        ["AI/ML", "126", "127", "281A", "188", "189", "227B", "227C", "288", "280", "182", "281B"],
        ["Theory", "127", "170", "Math 113", "172", "191", "174", "270", "271", "176", "294"],
        ["Graphics", "184", "194-26", "284B"],
        ["Design", "160", "169", "260B"],
        ["Architecture", "151", "152"],
        ["Systems", "267", "164", "149", "168", "162", "186", "264", "268", "261N", "122", "161", "261", "194-35", "262A", "262B"],
    ]

    ids = set(graph)
    for v in graph.values():
        ids.update(v)

    node_groups = dict()
    for i, g in enumerate(groups):
        i += 1  # Start at group 1
        for n in g:
            node_groups[n] = i

    nodes = [{"id": n, "group": node_groups[n]} for n in ids]

    links = []
    for s, es in graph.items():
        for e in es:
            links.append({
                "source": s,
                "target": e,
            })

    data = {
        "nodes": nodes,
        "links": links,
    }
    return JsonResponse(data)
