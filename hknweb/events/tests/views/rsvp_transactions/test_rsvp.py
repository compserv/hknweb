from django.test import TestCase

from django.urls import reverse

from hknweb.events.tests.models.utils import ModelFactory


class RsvpViewTests(TestCase):
    def test_no_event_types(self):
        pass
