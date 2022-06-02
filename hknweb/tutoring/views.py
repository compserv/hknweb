from typing import Dict

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static

from hknweb.utils import allow_public_access

from hknweb.tutoring.models import Slot, TutoringLogistics


@allow_public_access
def index(request):
    nav = request.GET.get("nav", "0")
    try:
        nav = int(nav)
    except ValueError:
        nav = 0

    context = {
        "offset": timezone.now() + timezone.timedelta(days=nav),
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
    slot_objs: QuerySet[Slot] = \
        logistics.slot_set \
            .filter(weekday=start.weekday()) \
            .prefetch_related("tutors")

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
