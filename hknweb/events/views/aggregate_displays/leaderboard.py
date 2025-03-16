from django.core.paginator import Paginator
from django.shortcuts import render
from hknweb.utils import allow_all_logged_in_users
from django.db.models import Count, Q
from django.contrib.auth.models import User
from hknweb.models import Committeeship

PAGE_SIZE = 20


@allow_all_logged_in_users
def get_leaderboard(request):
    query = request.GET.get("q", "")
    active = request.GET.get("active", "")
    res = User.objects.annotate(
        num_rsvps=Count("rsvp", filter=Q(rsvp__confirmed=True))
    ).order_by("-num_rsvps")

    # Search bar filter
    if query:
        res = res.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )

    # Current officer filter
    if active:
        curr_committeeships = Committeeship.objects.filter(
            Q(election__semester__semester="Spring") & Q(election__semester__year=2025)
        )

        curr_users = Committeeship.objects.none()
        for committeeship in curr_committeeships:
            curr_users |= committeeship.officers.all()
            curr_users |= committeeship.assistant_officers.all()
            curr_users |= committeeship.committee_members.all()

        res = res.filter(id__in=curr_users.distinct())

    paginator = Paginator(res, PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "query": query, "active": active}
    return render(request, "events/leaderboard.html", context)

