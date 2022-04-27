from django.core.paginator import Paginator
from django.shortcuts import render
from hknweb.utils import allow_all_logged_in_users
from django.db.models import Count, Q
from django.contrib.auth.models import User

PAGE_SIZE = 20


@allow_all_logged_in_users
def get_leaderboard(request):
    res = User.objects.annotate(
        num_rsvps=Count("rsvp", filter=Q(rsvp__confirmed=True))
    ).order_by("-num_rsvps")

    paginator = Paginator(res, PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "events/leaderboard.html", context)
