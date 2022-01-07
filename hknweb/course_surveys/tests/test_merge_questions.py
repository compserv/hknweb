import json

from django.test import TestCase

from django.urls import reverse

from hknweb.academics.models import Question, Rating
from hknweb.academics.tests.utils import ModelFactory

from hknweb.course_surveys.constants import Attr
from hknweb.course_surveys.tests.utils import (
    create_user_with_course_surveys_edit_permission,
)


class MergeQuestionViewTests(TestCase):
    def setUp(self):
        create_user_with_course_surveys_edit_permission(self)

    def test_returns_200(self):
        survey = ModelFactory.create_default_survey()

        N = 5
        questions = [ModelFactory.create_question() for _ in range(N)]

        for q in questions:
            ModelFactory.create_rating(q, survey)

        self.assertTrue(Rating.objects.count() == Question.objects.count() == N)

        question_ids = [str(q.id) for q in questions]
        question_ids_json = json.dumps(question_ids)
        base_url = reverse("course_surveys:merge_questions")
        url = base_url + "?" + Attr.QUESTION_IDS + "=" + question_ids_json
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Rating.objects.count(), N)
