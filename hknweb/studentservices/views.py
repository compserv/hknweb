from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from hknweb.utils import markdownify
from hknweb.events.views.aggregate_displays.calendar import calendar_helper
from hknweb.events.views.event_transactions.show_event import show_details_helper
from hknweb.utils import (
    allow_public_access,
    login_and_access_level,
    GROUP_TO_ACCESSLEVEL,
    login_and_committee,
)
from hknweb.studentservices.models import (
    CourseGuideNode,
    CourseGuideAdjacencyList,
    CourseGuideGroup,
    CourseGuideParam,
    CourseDescription,
)
from hknweb.studentservices.forms import DocumentForm, TourRequest, CourseEditForm


@allow_public_access
def resume_critique_submit(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    success = request.method == "POST" and form.is_valid()

    if success:
        form.save()
        messages.success(request, "Thank you for submitting your resume!")

    return render(
        request,
        "studentservices/resume_critique.html",
        {"form": form, "success": success},
    )


@allow_public_access
def reviewsessions(request):
    return calendar_helper(
        request, "Review Sessions", event_type_types=["Review Session"]
    )


@allow_public_access
def show_reviewsession_details(request, id):
    return show_details_helper(
        request, id, reverse("studentservices:reviewsessions"), False
    )


@allow_public_access
def tours(request):
    form = TourRequest(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()

            # Send deprel an email
            subject = "Department Tour Request"
            officer_email = "deprel@hkn.eecs.berkeley.edu"

            html_content = render_to_string(
                "studentservices/tour_request_email.html",
                {
                    "name": form.instance.name,
                    "datetime": form.instance.datetime,
                    "email": form.instance.email,
                    "phone": form.instance.phone,
                    "comments": form.instance.comments,
                },
            )
            msg = EmailMessage(
                subject, html_content, settings.NO_REPLY_EMAIL, [officer_email]
            )
            msg.content_subtype = "html"
            msg.send()

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

    context["groups"] = [
        g.name for g in CourseGuideGroup.objects.all() if g.name != "Core"
    ]

    return render(request, "studentservices/course_guide.html", context=context)


@allow_public_access
def course_guide_data(request):
    group_names_get = request.GET.get("groups", None)
    group_names_get = group_names_get.split(",") if group_names_get else []
    group_names_get.append("Core")

    groups = []
    group_names = []
    for group in CourseGuideGroup.objects.all():
        if group_names_get and group.name not in group_names_get:
            continue

        group_names.append(group.name)
        groups.append([node.name for node in group.nodes.all()])

    group_name_id = {
        g.name: (i + 1) for i, g in enumerate(CourseGuideGroup.objects.all())
    }

    node_groups = dict()
    for i, g in enumerate(groups):
        group_num = group_name_id.get(group_names[i], -1)
        for n in g:
            node_groups[n] = group_num

    graph = dict()
    for adjacency_list in CourseGuideAdjacencyList.objects.all():
        if adjacency_list.source.name not in node_groups:
            continue

        graph[adjacency_list.source.name] = [
            node.name
            for node in adjacency_list.targets.all()
            if node.name in node_groups
        ]

    course_surveys_link = reverse("course_surveys:index")
    link_template = f"{course_surveys_link}?search_by=courses&search_value="
    nodes = []
    for n in CourseGuideNode.objects.all():
        if n.name not in node_groups:
            continue

        node_attrs = {
            "id": n.name,
            "link": link_template + n.name,
            "title": n.is_title,
            "group": node_groups[n.name],
            "fx": n.x_0,
            "fy": n.y_0,
            "fixed": ((n.x_0 is not None) and (n.y_0 is not None)),
        }

        nodes.append(node_attrs)

    links = []
    for s, es in graph.items():
        for e in es:
            links.append(
                {
                    "source": s,
                    "target": e,
                    "source_group": node_groups[s],
                    "target_group": node_groups[e],
                }
            )

    data = {
        "nodes": nodes,
        "links": links,
    }
    return JsonResponse(data)


@allow_public_access
def course_description(request, slug):
    course = get_object_or_404(CourseDescription, slug=slug)
    context = {
        "course": course,
        "description": markdownify(course.description),
        "quick_links": markdownify(course.quick_links),
        "prerequisites": markdownify(course.prerequisites),
        "topics_covered": markdownify(course.topics_covered),
        "more_info": markdownify(course.more_info),
    }
    return render(request, "studentservices/course_description.html", context=context)


@login_and_committee(settings.TUTORING_GROUP)
def edit_description(request, slug):
    course = get_object_or_404(CourseDescription, slug=slug)
    if request.method == "GET":
        form = CourseEditForm(instance=course)
    elif request.method == "POST":
        form = CourseEditForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("studentservices:course_description", slug=slug)

    context = {
        "course": course,
        "form": form,
    }

    return render(request, "studentservices/course_edit.html", context=context)


@login_and_committee(settings.TUTORING_GROUP)
def delete_description(request, slug):
    course = get_object_or_404(CourseDescription, slug=slug)

    if request.method == "POST":
        course.delete()

    return redirect("tutoring:courses")
