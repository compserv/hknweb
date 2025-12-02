from hknweb.candidate.views.candidate_portal import (
    candidate_portal,
    candidate_portal_view_by_username,
)
from hknweb.candidate.views.officer_portal import officer_portal
from hknweb.candidate.views.form_request import request_bitbyte, request_challenge
from hknweb.candidate.views.confirm_request import (
    confirm_challenge,
    confirm_bitbyte,
    checkoff_req,
    checkoff_event,
)
from hknweb.candidate.views.autocomplete import OfficerAutocomplete, UserAutocomplete
from hknweb.candidate.views.shortlinks import (
    manage_shortlinks,
    create_shortlink,
    import_shortlinks,
    redirect_shortlink,
)
