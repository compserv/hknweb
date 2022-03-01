from django.shortcuts import render
from django.contrib.auth.models import User

from hknweb.utils import login_and_permission
from hknweb.candidate.utils_candportal import CandidatePortalData


@login_and_permission("candidate.change_offchallenge")
def summary(request):
    cands = User.objects.filter(groups__name="candidate")
    headers, rows = [], []
    for cand in cands:
        data = CandidatePortalData(cand).get_user_cand_data()

        if not headers:
            headers = [
                "Name",
                "Forms",
                "Payments",
                "Project",
                "BitByte",
                "Hangouts",
            ]
            for event in data["events"]:
                event_title = event["title"]
                if len(event_title) > 15:
                    event_title = event_title.split()[0]
                headers.append(event_title)
            headers.append("Overall")

        status = [
            data["candidate_forms"]["all_done"],
            data["due_payments"]["all_done"],
            data["committee_project"]["all_done"],
            data["bitbyte"]["status"],
            data["interactivities"]["status"],
            *(e["status"] for e in data["events"]),
        ]
        status.append(all(status))

        row = {
            "name": f"{cand.first_name} {cand.last_name} ({cand.username})",
            "status": status,
            "link": f"/cand/portal/{cand.username}",
        }
        rows.append(row)

    context = {
        "headers": headers,
        "rows": rows,
    }
    return render(request, "candidate/summary.html", context=context)
