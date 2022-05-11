from typing import DefaultDict, Tuple, List, Dict, Union
from collections import Counter, defaultdict

from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count, QuerySet, F

from hknweb.utils import login_and_access_level, GROUP_TO_ACCESSLEVEL
from hknweb.events.models import Rsvp

from hknweb.candidate.models import OffChallenge, BitByteActivity, Logistics
from hknweb.candidate.views.candidate_portal import get_logistics


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def officer_portal(request):
    context = {
        "logistics": {
            "challenges": OffChallenge.objects.filter(
                officer__exact=request.user
            ).order_by("-request_date"),
            "bitbytes": BitByteActivity.objects.filter(
                participants__exact=request.user
            ).order_by("-request_date"),
        },
    }

    logistics = get_logistics()
    if not logistics:
        return render(request, "candidate/officer_portal.html", context)

    candidates = User.objects.filter(groups__name="candidate")

    challenges = Bulk.challenges(candidates)
    hangouts = Bulk.hangouts(candidates)
    interactivites = challenges + hangouts
    bitbytes = Bulk.bitbytes(candidates)

    event_reqs, event_req_minimums = Bulk.event_reqs(candidates, logistics)
    form_reqs = Bulk.form_reqs(logistics)
    misc_reqs = Bulk.misc_reqs(logistics)

    reqs = list(event_reqs) + list(form_reqs) + list(misc_reqs)
    headers = ["Challenges", "Hangouts", "Interactivities", "BitByte"] + reqs
    minimums = \
        [
            logistics.min_challenges,
            logistics.min_hangouts,
            logistics.num_interactivities,
            logistics.num_bitbyte,
        ] \
        + event_req_minimums

    summary_statuses = [0] * (len(headers) + 1)
    rows = []
    for c in candidates:
        c_id = c.id
        checkoffable_statuses, checkoffs = get_checkoff_info(
            logistics, c_id, form_reqs, misc_reqs
        )
        statuses = [
            challenges[c_id],
            hangouts[c_id],
            interactivites[c_id],
            bitbytes[c_id],
            *[c[c_id] for c in event_reqs.values()],
        ]
        finished = [n_finished >= n_required for n_finished, n_required in zip(statuses, minimums)]
        overall_status = all(finished) and all(checkoffable_statuses)

        for i in range(len(finished)):
            summary_statuses[i+1] += finished[i]
        for j in range(len(checkoffable_statuses)):
            summary_statuses[(i+1) + (j+1)] += checkoffable_statuses[j]
        summary_statuses[0] += overall_status

        rows.append(
            {
                "username": c.username,
                "name": f"{c.first_name} {c.last_name}",
                "overall": overall_status,
                "statuses": statuses,
                "checkoffs": checkoffs,
            }
        )

    context.update(
        {
            "headers": headers,
            "rows": rows,
            "summary": summary_statuses,
            "minimums": minimums,
        }
    )
    return render(request, "candidate/officer_portal.html", context)


def get_checkoff_info(
    logistics: Logistics,
    c_id: int,
    form_reqs: DefaultDict[str, set],
    misc_reqs: DefaultDict[str, set],
) -> Tuple[List[bool], List[Dict[str, Union[str, int]]]]:
    form_req_statuses = [c_id in f for f in form_reqs.values()]
    misc_req_statuses = [c_id in m for m in misc_reqs.values()]

    info = [
        ("form_req", form_reqs, form_req_statuses),
        ("misc_req", misc_reqs, misc_req_statuses),
    ]
    checkoffs = []
    for type, reqs, statuses in info:
        for title, s in zip(reqs, statuses):
            checkoffs.append(
                {
                    "logistics_id": logistics.id,
                    "type": type,
                    "obj_title": title,
                    "user_id": c_id,
                    "operation": int(s),
                    "status": s,
                }
            )

    statuses = form_req_statuses + misc_req_statuses
    return statuses, checkoffs


class Bulk:
    @staticmethod
    def challenges(candidates: QuerySet) -> Counter:
        challenges = (
            OffChallenge.objects.filter(
                requester__in=candidates,
                officer_confirmed=True,
            )
            .values_list("requester")
            .annotate(Count("requester"))
        )
        return Counter(dict(challenges))

    @staticmethod
    def hangouts(candidates: QuerySet) -> Counter:
        hangouts = (
            Rsvp.objects.filter(
                event__event_type__type="Hangout",
                user__in=candidates,
                confirmed=True,
            )
            .values_list("user")
            .annotate(Count("user"))
        )
        return Counter(dict(hangouts))

    @staticmethod
    def bitbytes(candidates: QuerySet) -> Counter:
        bitbytes = (
            BitByteActivity.objects.filter(
                participants__in=candidates,
                confirmed=True,
            )
            .values_list("participants")
            .annotate(Count("participants"))
        )
        return Counter(dict(bitbytes))

    @staticmethod
    def event_reqs(
        candidates: QuerySet, logistics: Logistics
    ) -> Union[DefaultDict[str, Counter], List[int]]:
        candidate_rsvps = (
            Rsvp.objects.filter(
                confirmed=True,
                user__in=candidates,
            )
            .values_list("event__event_type__type", "user__id")
            .annotate(count=Count(F("event__event_type__type") + F("user__id")))
        )

        events_info = defaultdict(Counter)
        for t, u, c in candidate_rsvps:
            events_info[t][u] = c

        event_reqs, event_req_minumums = defaultdict(set), []
        for event_req in logistics.event_reqs.all().prefetch_related("event_types"):
            counts = Counter()
            for event_type in event_req.event_types.all():
                counts += events_info[event_type.type]
            event_reqs[event_req.title] = counts
            event_req_minumums.append(event_req.n)

        return event_reqs, event_req_minumums

    @staticmethod
    def _reqs_helper(reqs: QuerySet) -> DefaultDict[str, set]:
        res: DefaultDict[int, set] = defaultdict(set)
        misc_reqs = reqs.values_list("title", "completed")
        for m_id, c_id in misc_reqs:
            if not c_id:
                res[m_id]
            else:
                res[m_id].add(c_id)
        return res

    @staticmethod
    def form_reqs(logistics: Logistics) -> DefaultDict[str, set]:
        return Bulk._reqs_helper(logistics.form_reqs)

    @staticmethod
    def misc_reqs(logistics: Logistics) -> DefaultDict[str, set]:
        return Bulk._reqs_helper(logistics.misc_reqs)
