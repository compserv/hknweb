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
        test_dir = "media/tutoring-algorithm/test/"

        # Load target experiment results
        prev_results_strs = open(test_dir + "exp_results.txt").readlines()[-8:]
        parse_result = lambda s: (s[:2], int(s[8:11]))
        prev_results = dict(map(parse_result, prev_results_strs))

        # Run experiments
        test_template = test_dir + "s{}.json"
        scores = []
        for i in range(1, 7+1):
            path = test_template.format(str(i))
            data: Data = LocalJSONData(path)
            score = schedule(data, output_readable=False)

            scores.append(score)

        print("Dataset target_score current_score off_by")
        for i, score in enumerate(scores):
            name = f"s{i+1}"
            prev_score = prev_results[name]
            off_by = 1 - (prev_score / score)
            print(f"{name}: {prev_score} {int(score)} {off_by}")
