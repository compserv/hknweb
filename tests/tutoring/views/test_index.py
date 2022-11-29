from django.test import TestCase

from django.urls import reverse
from django.utils import timezone

from hknweb.tutoring.models import Room, Semester, Slot, TutoringLogistics


class TuteeViewTestHelper(TestCase):
    def setUp(self):
        self.semester: Semester = Semester.objects.create(semester="Fa", year=2000)
        self.logistics: TutoringLogistics = TutoringLogistics.objects.create(
            semester=self.semester
        )
        self.room: Room = Room.objects.create(name="test_room", color="gray")
        self.slot: Slot = Slot.objects.create(
            logistics=self.logistics,
            room=self.room,
            num_tutors=2,
            weekday=timezone.now().weekday(),
            time=timezone.now().time(),
        )


class IndexViewTests(TuteeViewTestHelper):
    def test_index_returns_200(self):
        response = self.client.get(reverse("tutoring:index"))

        self.assertEqual(response.status_code, 200)
