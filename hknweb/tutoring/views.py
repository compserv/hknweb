from typing import Dict, List

from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static

from dal import autocomplete

from hknweb.utils import allow_public_access

from hknweb.coursesemester.models import Course
from hknweb.tutoring.models import Slot, TutoringLogistics
from hknweb.tutoring.forms import CourseFilterForm


@allow_public_access
def index(request):
    nav = request.GET.get("nav", "0")
    try:
        nav = int(nav)
    except ValueError:
        nav = 0

    context = {
        "offset": timezone.now() + timezone.timedelta(days=nav),
        "form": CourseFilterForm(),
    }

    return render(request, "tutoring/index.html", context=context)


@allow_public_access
def slots(request):
    logistics: TutoringLogistics = TutoringLogistics.objects \
        .order_by("-semester__year", "semester__semester") \
        .first()
    if logistics is None:
        return JsonResponse({})

    start = timezone.datetime.fromisoformat(request.GET.get("start"))
    try:
        course_ids: List[int] = list(map(int, request.GET.get("course_filter", "").split(",")))
    except ValueError:
        course_ids: List[int] = []
    course_filter_kwargs: Dict[str, List[int]] = {}
    if course_ids:
        course_filter_kwargs = {"tutors__profile__preferred_courses__in": course_ids}

    slot_objs: QuerySet[Slot] = \
        logistics.slot_set \
            .filter(weekday=start.weekday(), **course_filter_kwargs) \
            .distinct() \
            .prefetch_related("tutors", "room", "tutors__profile", "tutors__profile__preferred_courses")

    blank_pic_url = static("img/blank_profile_pic.jpg")
    def serialize_tutor(tutor: User) -> Dict[str, str]:
        return {
            "picture": tutor.profile.picture_display_url() if tutor.profile.picture else blank_pic_url,
            "name": tutor.get_full_name(),
            "courses": tutor.profile.preferred_courses_str(),
        }


    def serialize_slot(slot: Slot) -> Dict[str, str]:
        start_time = timezone.datetime.combine(start.date(), slot.time)
        end_time = start_time + timezone.timedelta(hours=1)
        return {
            "title": slot.tutor_names(),
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "color": slot.room.color,
            "id": f'slot{slot.id}',
            "tooltip_title": f'{start_time.strftime("%I:%M%p")} - {end_time.strftime("%I:%M%p")} in {slot.room.name}',
            "tutors": list(map(serialize_tutor, slot.tutors.all())),
        }

    slots = list(map(serialize_slot, slot_objs))
    return JsonResponse(slots, safe=False)


class CourseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        courses = Course.objects
        if self.q:
            courses = courses.filter(
                Q(name__icontains=self.q)
                | Q(number__icontains=self.q)
                | Q(department__abbreviated_name__icontains=self.q)
                | Q(department__long_name__icontains=self.q)
            )
        return courses.order_by("number", "department__abbreviated_name")


course_autocomplete = allow_public_access(CourseAutocomplete.as_view())
