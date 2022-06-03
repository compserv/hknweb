from typing import Dict, List

from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static

from hknweb.utils import allow_public_access

from hknweb.tutoring.models import Slot, TutoringLogistics


@allow_public_access
def slots(request):
    logistics: TutoringLogistics = TutoringLogistics.objects \
        .order_by("-semester__year", "semester__semester") \
        .first()
    if logistics is None:
        return JsonResponse({})

    start = timezone.datetime.fromisoformat(request.GET.get("start"))

    def get_filter_params(param_name: str, kwarg_name: str) -> Dict[str, List[int]]:
        try:
            param_ids: List[int] = list(map(int, request.GET.get(param_name, "").split(",")))
        except ValueError:
            param_ids: List[int] = []
        param_filter_kwargs: Dict[str, List[int]] = {}
        if param_ids:
            param_filter_kwargs = {kwarg_name: param_ids}

        return param_filter_kwargs


    course_filter_kwargs = get_filter_params(
        "course_filter", "tutors__profile__preferred_courses__in"
    )
    tutor_filter_kwargs = get_filter_params("tutor_filter", "tutors__in")

    slot_objs: QuerySet[Slot] = \
        logistics.slot_set \
            .filter(weekday=start.weekday(), **course_filter_kwargs, **tutor_filter_kwargs) \
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
