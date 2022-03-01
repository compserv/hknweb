from django.views import generic

from hknweb.utils import method_login_and_permission

from hknweb.candidate.models import OffChallenge


@method_login_and_permission("candidate.view_offchallenge")
class OfficerPortalView(generic.ListView):
    """Officer portal.
    List of past challenge requests for officer.
    Non-officers can still visit this page by typing in the url,
    but it will not have any new entries. Option to add
    new candidates."""

    template_name = "candidate/officer_portal.html"

    context_object_name = "challenge_list"

    def get_queryset(self):
        result = OffChallenge.objects.filter(officer__exact=self.request.user).order_by(
            "-request_date"
        )
        return result
