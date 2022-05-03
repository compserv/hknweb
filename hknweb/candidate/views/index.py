from django.views import generic

from hknweb.utils import method_login_and_permission


@method_login_and_permission("candidate.view_announcement")
class IndexView(generic.TemplateView):
    """Candidate portal home."""

    template_name = "candidate/index.html"

    def get_context_data(self):
        return {}
