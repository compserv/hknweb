from django.test import TestCase

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.urls import reverse

from hknweb.events.models import Rsvp

from hknweb.events.tests.models.utils import ModelFactory


class TabularViewTests(TestCase):
    def test_returns_200(self):
        user = ModelFactory.create_user()
        password = "custom password"
        user.set_password(password)
        user.save()

        content_type = ContentType.objects.get_for_model(Rsvp)
        permission = Permission.objects.get(content_type=content_type, codename="add_rsvp")
        user.user_permissions.add(permission)

        self.client.login(username=user.username, password=password)

        response = self.client.get(reverse("events:rsvps"))

        self.assertEqual(response.status_code, 200)
