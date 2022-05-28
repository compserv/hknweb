"""
These tests are not run as part of the regular website test suite.

Instead, use the below command to run them manually.
```
HKNWEB_MODE='dev' python manage.py test hknweb.tutoring.tests.scheduler
```
"""
import random

from django.test import TestCase

from hknweb.tutoring.scheduler.data import Data, LocalJSONData, RemoteJSONData
from hknweb.tutoring.scheduler.schedule import schedule


class SchedulerTests(TestCase):
    SEED = 42

    def setUp(self):
        random.seed(self.SEED)

    def test_scheduler_url(self):
        url = "https://raw.githubusercontent.com/compserv/tutoring-algorithm/master/test/s1.json"
        data: Data = RemoteJSONData(url)
        schedule(data)

    def test_scheduler_local(self):
        test_template = "media/tutoring-algorithm/test/s{}.json"
        scores = []
        for i in range(1, 7+1):
            path = test_template.format(str(i))
            data: Data = LocalJSONData(path)
            score = schedule(data, output_readable=False)

            scores.append(score)

        for i, score in enumerate(scores):
            print(f"s{i}: {score:.d}")
