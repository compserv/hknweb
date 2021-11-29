from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class EventRequirementModelTests(TestCase):
    def setUp(self):
        event_type = ModelFactory.create_eventtype(type="custom event type")
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        event_requirement = ModelFactory.create_event_requirement(
            eventType=event_type,
            candidateSemesterActive=semester,
            enableTitle=True,
        )

        self.event_type = event_type
        self.semester = semester
        self.event_requirement = event_requirement

    def test_str(self):
        expected = "{} {} Event - Number Required: {}{}".format(
            self.semester,
            "{} ({})".format(self.event_requirement.title, self.event_type),
            self.event_requirement.numberRequired,
            " [Off]",
        )
        actual = str(self.event_requirement)

        self.assertEqual(expected, actual)
