"""
These tests are not run as part of the regular website test suite.

Instead, use the below command to run them manually.
```
HKNWEB_MODE='dev' python manage.py test hknweb.tutoring.tests.scheduler
```
"""

from django.test import TestCase

from hknweb.tutoring.scheduler.data import Data, OldJSONTestData
from hknweb.tutoring.scheduler.schedule import schedule


class SchedulerTests(TestCase):
    def test_scheduler(self):
        url = "https://raw.githubusercontent.com/compserv/tutoring-algorithm/master/test/s1.json"
        data: Data = OldJSONTestData(url)
        schedule(data)
