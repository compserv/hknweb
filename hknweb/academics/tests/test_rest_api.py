from django.test import TestCase

from hknweb.academics.tests.utils import login_user


class RESTAPITests(TestCase):
    def setUp(self):
        login_user(self)

    def test_basic(self):
        paths = [
            "",
            "questions/",
            "ratings/",
            "surveys/",
            "icsrs/",
            "courses/",
            "departments/",
            "instructors/",
            "semesters/",
        ]

        for path in paths:
            response = self.client.get("/academics/api/{path}".format(path=path))

            self.assertEqual(response.status_code, 200)
