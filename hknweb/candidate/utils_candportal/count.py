from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone

from hknweb.utils import get_semester_bounds
from hknweb.coursesemester.models import Semester

from hknweb.candidate.constants import ATTR, EVENT_NAMES
from hknweb.candidate.models import (
    BitByteActivity,
    OffChallenge,
    RequirementBitByteActivity,
    RequirementHangout,
)


def count_challenges(requested_user: User, candidate_semester: Semester) -> dict:
    challenges = OffChallenge.objects.filter(requester__exact=requested_user)
    r = (
        candidate_semester
        and RequirementHangout.objects.filter(
            eventType=EVENT_NAMES.CHALLENGE,
            candidateSemesterActive=candidate_semester,
            enable=True
        ).first()
    )

    start_time, end_time = get_semester_bounds(timezone.now())
    if r is not None:
        challenges = challenges.filter(
            request_date__gt=r.hangoutsDateStart or start_time,
            request_date__lt=r.hangoutsDateEnd or end_time,
        )

    confirmed = challenges.filter(
        Q(officer_confirmed=True) & Q(csec_confirmed=True)
    ).count()
    rejected = challenges.filter(
        Q(officer_confirmed=False) | Q(csec_confirmed=False)
    ).count()
    pending = challenges.count() - confirmed - rejected

    return {
        ATTR.NUM_PENDING: pending,
        ATTR.NUM_REJECTED: rejected,
        ATTR.NUM_CONFIRMED: confirmed,
    }


def count_num_bitbytes(
    requested_user: User,
    candidate_semester: Semester,
) -> int:
    r = (
        candidate_semester
        and RequirementBitByteActivity.objects.filter(
            candidateSemesterActive=candidate_semester,
            enable=True
        ).first()
    )

    start_time, end_time = get_semester_bounds(timezone.now())
    return BitByteActivity.objects.filter(
        participants__exact=requested_user,
        confirmed=True,
        request_date__gt=(r and r.bitByteDateStart) or start_time,
        request_date__lt=(r and r.bitByteDateEnd) or end_time,
    ).count()
