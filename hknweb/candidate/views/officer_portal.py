from django.shortcuts import render
from django.contrib.auth.models import User

from hknweb.utils import login_and_access_level, GROUP_TO_ACCESSLEVEL

from hknweb.candidate.models import OffChallenge, BitByteActivity
from hknweb.candidate.views.candidate_portal import user_candidate_portal


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def officer_portal(request):
    challenges = OffChallenge.objects.filter(officer__exact=request.user).order_by(
        "-request_date"
    )

    bitbytes = BitByteActivity.objects.filter(
        participants__exact=request.user
    ).order_by("-request_date")

    rows = []
    for c in User.objects.filter(groups__name="candidate"):
        info = user_candidate_portal(c)
        logistics = info["logistics"]
        statuses = [
            logistics.n_challenges_confirmed >= logistics.min_challenges,
            len(logistics.hangouts_confirmed) >= logistics.min_hangouts,
            logistics.n_interactivities >= logistics.num_interactivities,
            logistics.n_bitbyte >= logistics.num_bitbyte,
            *[e.n_finished >= e.n for e in logistics.event_req_objs],
            *[c in f.completed.all() for f in logistics.form_reqs.all()],
            *[c in m.completed.all() for m in logistics.misc_reqs.all()],
        ]
        rows.append(
            {
                "username": info["username"],
                "name": f"{c.first_name} {c.last_name}",
                "overall": all(statuses),
                "statuses": statuses,
            }
        )

    headers = []
    if rows:
        headers = (
            ["Challenges", "Hangouts", "Interactivities", "BitByte"]
            + [e.title for e in logistics.event_req_objs]
            + [f.title for f in logistics.form_reqs.all()]
            + [m.title for m in logistics.misc_reqs.all()]
        )

    context = {
        "logistics": {
            "challenges": challenges,
            "bitbytes": bitbytes,
        },
        "headers": headers,
        "rows": rows,
    }
    return render(request, "candidate/officer_portal.html", context)
