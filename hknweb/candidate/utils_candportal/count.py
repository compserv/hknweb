from django.conf import settings
from django.db.models import Q
from hknweb.candidate.models import (
    BitByteActivity,
    OffChallenge,
    RequirementHangout,
)


def count_challenges(requested_user, candidateSemester):
    challenges = OffChallenge.objects.filter(requester__exact=requested_user)
    req_challenges_models = RequirementHangout.objects.filter(
        eventType=settings.CHALLENGE_ATTRIBUTE_NAME,
        candidateSemesterActive=candidateSemester,
    ).first()
    if req_challenges_models is not None:
        if req_challenges_models.hangoutsDateStart is not None:
            challenges = challenges.filter(
                request_date__gt=req_challenges_models.hangoutsDateStart,
            )
        if req_challenges_models.hangoutsDateEnd is not None:
            challenges = challenges.filter(
                request_date__lt=req_challenges_models.hangoutsDateEnd,
            )
    # if either one is waiting, challenge is still being reviewed

    ## Count number of confirmed
    challenges_confirmed = challenges.filter(
        Q(officer_confirmed=True) & Q(csec_confirmed=True)
    )
    num_challenges_confirmed = challenges_confirmed.count()
    ##

    ## Count number of rejected
    challenges_rejected = challenges.filter(
        Q(officer_confirmed=False) | Q(csec_confirmed=False)
    )
    num_challenges_rejected = challenges_rejected.count()
    ##

    num_pending = (
        challenges.count() - num_challenges_confirmed - num_challenges_rejected
    )

    return num_challenges_confirmed, num_challenges_rejected, num_pending


def count_num_bitbytes(requested_user, bitbyte_requirement):
    bitbyte_models = BitByteActivity.objects.filter(
        participants__exact=requested_user, confirmed=True
    )
    if bitbyte_requirement is not None:
        if bitbyte_requirement.bitByteDateStart is not None:
            bitbyte_models = bitbyte_models.filter(
                request_date__gt=bitbyte_requirement.bitByteDateStart,
            )
        if bitbyte_requirement.bitByteDateEnd is not None:
            bitbyte_models = bitbyte_models.filter(
                request_date__lt=bitbyte_requirement.bitByteDateEnd,
            )
    num_bitbytes = bitbyte_models.count()
    return num_bitbytes
