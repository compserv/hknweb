from django.conf import settings
from django.test import TestCase, RequestFactory
from django.http import HttpResponse

from collections import namedtuple
from django.core.exceptions import PermissionDenied
from tests.events.models.utils import ModelFactory
from django.contrib.auth.models import Group, AnonymousUser
from hknweb.utils import login_and_committee, login_and_exec


class UsersGroupsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cand = ModelFactory.create_user(username="cand")
        cls.officer = ModelFactory.create_user(username="officer")
        cls.exec = ModelFactory.create_user(username="exec")
        cls.bridge = ModelFactory.create_user(username="bridge")
        cls.tutoring = ModelFactory.create_user(username="tutoring")
        cls.csec = ModelFactory.create_user(username="csec")
        cls.pres = ModelFactory.create_user(username="pres")
        cls.anon = AnonymousUser()

        data = namedtuple("data", "user group bridge tutoring csec pres")

        cls.user_data = (
            data(cls.cand, settings.CAND_GROUP, 403, 403, 403, 403),
            data(cls.officer, settings.OFFICER_GROUP, 403, 403, 403, 403),
            data(cls.exec, settings.EXEC_GROUP, 200, 200, 403, 403),
            data(cls.bridge, settings.BRIDGE_GROUP, 200, 403, 403, 403),
            data(cls.tutoring, settings.TUTORING_GROUP, 403, 200, 403, 403),
            data(cls.csec, settings.CSEC_GROUP, 403, 403, 200, 403),
            data(cls.pres, settings.PRES_GROUP, 403, 403, 403, 200),
            data(cls.anon, None, 302, 302, 302, 302),
        )

        for curr in cls.user_data:
            if curr.user == cls.anon:
                continue
            curr_group = Group.objects.create(name=curr.group)
            curr.user.groups.add(curr_group)

    def setUp(self):
        # https://docs.djangoproject.com/en/5.1/topics/testing/advanced/#django.test.RequestFactory

        self.factory = RequestFactory()

    def test_bridge_committee_req(self):
        @login_and_committee(settings.BRIDGE_GROUP)
        def bridge_test_view(request):
            return HttpResponse("Access Granted")

        for data in self.user_data:
            user = data.user
            target_status = data.bridge
            with self.subTest(
                Username=getattr(user, "username", "anon"), goal=target_status
            ):
                request = self.factory.get("/test-bridge/")
                request.user = user
                if target_status == 403:
                    with self.assertRaises(PermissionDenied):
                        bridge_test_view(request)
                else:
                    response = bridge_test_view(request)
                    self.assertEqual(response.status_code, target_status)

    def test_tutoring_committee_req(self):
        @login_and_committee(settings.TUTORING_GROUP)
        def tutoring_test_view(request):
            return HttpResponse("Access Granted")

        for data in self.user_data:
            user = data.user
            target_status = data.tutoring
            with self.subTest(
                Username=getattr(user, "username", "anon"), goal=target_status
            ):
                request = self.factory.get("/test-tutoring/")
                request.user = user
                if target_status == 403:
                    with self.assertRaises(PermissionDenied):
                        tutoring_test_view(request)
                else:
                    response = tutoring_test_view(request)
                    self.assertEqual(response.status_code, target_status)

    def test_csec_exec_req(self):
        @login_and_exec(settings.CSEC_GROUP)
        def csec_test_view(request):
            return HttpResponse("Access Granted")

        for data in self.user_data:
            user = data.user
            target_status = data.csec
            with self.subTest(
                Username=getattr(user, "username", "anon"), goal=target_status
            ):
                request = self.factory.get("/test-csec/")
                request.user = user
                if target_status == 403:
                    with self.assertRaises(PermissionDenied):
                        csec_test_view(request)
                else:
                    response = csec_test_view(request)
                    self.assertEqual(response.status_code, target_status)

    def test_pres_exec_req(self):
        @login_and_exec(settings.PRES_GROUP)
        def pres_test_view(request):
            return HttpResponse("Access Granted")

        for data in self.user_data:
            user = data.user
            target_status = data.pres
            with self.subTest(
                Username=getattr(user, "username", "anon"), goal=target_status
            ):
                request = self.factory.get("/test-pres/")
                request.user = user
                if target_status == 403:
                    with self.assertRaises(PermissionDenied):
                        pres_test_view(request)
                else:
                    response = pres_test_view(request)
                    self.assertEqual(response.status_code, target_status)
