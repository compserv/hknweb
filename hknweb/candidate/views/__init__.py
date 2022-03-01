from hknweb.candidate.views.autocomplete import OfficerAutocomplete, UserAutocomplete
from hknweb.candidate.views.checkoffs import MemberCheckoffView, checkoff_csv
from hknweb.candidate.views.mass_add_cands import (
    create_candidates_view,
    add_cands,
    check_mass_candidate_status,
)
from hknweb.candidate.views.index import IndexView
from hknweb.candidate.views.officer_challenge import (
    officer_confirm_view,
    confirm_challenge,
    officer_review_confirmation,
    CandRequestView,
    challenge_detail_view,
)
from hknweb.candidate.views.officer_portal import OfficerPortalView
from hknweb.candidate.views.bitbyte import BitByteView
from hknweb.candidate.views.view_by_username import candidate_portal_view_by_username
from hknweb.candidate.views.summary import summary
