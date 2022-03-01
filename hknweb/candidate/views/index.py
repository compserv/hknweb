from django.views import generic

from hknweb.utils import method_login_and_permission

from hknweb.candidate.utils_candportal import CandidatePortalData


@method_login_and_permission("candidate.view_announcement")
class IndexView(generic.TemplateView):
    """Candidate portal home."""

    template_name = "candidate/index.html"
    context_object_name = "my_favorite_publishers"

    def get_context_data(self):
        cand_data = CandidatePortalData(self.request.user)
        return cand_data.get_user_cand_data()
