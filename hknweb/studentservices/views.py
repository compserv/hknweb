from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.views import generic
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from hknweb.utils import allow_public_access, login_and_permission, method_login_and_permission

from hknweb.studentservices.models import (
    DepTour,
    ReviewSession,
    CourseGuideNode,
    CourseGuideAdjacencyList,
    CourseGuideGroup,
    CourseGuideParam,
)
from hknweb.studentservices.forms import (
    DocumentForm,
    ReviewSessionForm,
    ReviewSessionUpdateForm,
    TourRequest,
)


@allow_public_access
def resume_critique_submit(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    success = request.method == "POST" and form.is_valid()

    if success:
        form.save()
        messages.success(request, "Thank you for submitting your resume!")

    return render(
        request, "studentservices/resume_critique.html", {"form": form, "success": success},
    )


@allow_public_access
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


@allow_public_access
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


@allow_public_access
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


@allow_public_access
def course_guide(request):
    context = dict()

    if CourseGuideParam.objects.exists():
        context["params"] = CourseGuideParam.objects.first().to_dict()

    context["groups"] = [g.name for g in CourseGuideGroup.objects.all() if g.name != "Core"]

    return render(request, "studentservices/course_guide.html", context=context)


@allow_public_access
def course_guide_data(request):
    group_names = request.GET.get("groups", None)
    group_names = group_names.split(",") if group_names else []
    group_names.append("Core")

    groups = []
    for group in CourseGuideGroup.objects.all():
        if group_names and group.name not in group_names:
            continue

        groups.append([node.name for node in group.nodes.all()])

    node_groups = dict()
    for i, g in enumerate(groups):
        i += 1  # Start at group 1
        for n in g:
            node_groups[n] = i

    graph = dict()
    for adjacency_list in CourseGuideAdjacencyList.objects.all():
        if adjacency_list.source.name not in node_groups:
            continue

        graph[adjacency_list.source.name] = [
            node.name for node in adjacency_list.targets.all() if node.name in node_groups
        ]

    course_surveys_link = reverse("course_surveys:index")
    link_template = f"{course_surveys_link}?search_by=courses&search_value="
    nodes = []
    for n in CourseGuideNode.objects.all():
        if n.name not in node_groups:
            continue

        nodes.append({
            "id": n.name,
            "link": link_template + n.name,
            "title": n.is_title,
            "group": node_groups[n.name],
            "fx": n.x_0,
            "fy": n.y_0,
        })

    links = []
    for s, es in graph.items():
        for e in es:
            links.append({
                "source": s,
                "target": e,
                "source_group": node_groups[s],
                "target_group": node_groups[e],
            })

    data = {
        "nodes": nodes,
        "links": links,
    }
    return JsonResponse(data)
