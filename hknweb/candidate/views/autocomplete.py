from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q

from dal import autocomplete

from hknweb.utils import method_login_and_permission


# this is needed otherwise anyone can see the users in the database
@method_login_and_permission("auth.view_user")
class OfficerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(groups__name=settings.OFFICER_GROUP)
        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q)
                | Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
            )
        return qs


# this is needed otherwise anyone can see the users in the database
@method_login_and_permission("auth.view_user")
class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q)
                | Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
            )
        return qs
