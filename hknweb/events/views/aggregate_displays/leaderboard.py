from django.core.paginator import Paginator
from django.shortcuts import render

from hknweb.events.models import Rsvp


PAGE_SIZE = 20


def get_leaderboard(request):
    confirmed_rsvps = Rsvp.objects.all()
    user_to_events = {}
    for rsvp in confirmed_rsvps:
        if rsvp.confirmed:
            if rsvp.user in user_to_events:
                user_to_events[rsvp.user] += 1
            else:
                user_to_events[rsvp.user] = 1
    sorted_list = [
        (k, v)
        for k, v in sorted(
            user_to_events.items(), key=lambda item: item[1], reverse=True
        )
    ]

    paginator = Paginator(sorted_list, PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "events/leaderboard.html", context)
