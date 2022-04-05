from django.test import TestCase
from django.contrib.auth.models import Group

from hknweb.events.tests.models.utils import ModelFactory
from hknweb.init_permissions import provision


class CandidateViewTestsBase(TestCase):
    def setUp(self):
        password = "custom password"
        candidate = ModelFactory.create_user(
            username="test_candidate",
            email="test_candidate@berkeley.edu",
            first_name="test",
            last_name="candidate",
        )
        candidate.set_password(password)
        candidate.save()
        officer = ModelFactory.create_user(
            username="test_officer1",
            email="test_officer1@berkeley.edu",
            first_name="test",
            last_name="officer1",
        )
        officer.set_password(password)
        officer.save()
        officer2 = ModelFactory.create_user(
            username="test_officer2",
            email="test_officer2@berkeley.edu",
            first_name="test",
            last_name="officer2",
        )
        officer2.set_password(password)
        officer2.save()

        provision()

        candidate_group = Group.objects.get(name="candidate")
        candidate_group.user_set.add(candidate)
        candidate_group.save()
        officer_group = Group.objects.get(name="officer")
        officer_group.user_set.add(officer)
        officer_group.user_set.add(officer2)
        officer_group.save()

        self.password = password
        self.candidate = candidate
        self.officer = officer
        self.officer2 = officer2
