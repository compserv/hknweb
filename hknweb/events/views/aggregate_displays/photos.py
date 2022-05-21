from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render
from hknweb.utils import login_and_access_level, GROUP_TO_ACCESSLEVEL
from django.db.models import Count, Q, QuerySet

from hknweb.events.models import EventPhoto


PAGE_SIZE = 20


@login_and_access_level(GROUP_TO_ACCESSLEVEL["member"])
def photos(request):
    eventphoto_objs = EventPhoto.objects \
        .filter(event__end_time__lt=timezone.now()) \
        .order_by("-event__end_time")

    paginator = Paginator(eventphoto_objs, PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "events/photos.html", context)
