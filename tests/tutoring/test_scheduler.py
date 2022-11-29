"""
These tests are not run as part of the regular website test suite.

Instead, use the below command to run them manually.
```
python manage.py test tests.tutoring.test_scheduler
```
"""
import random
from typing import Callable, List
import requests
import os

from django.test import TestCase

from hknweb.tutoring.scheduler.data import Data, LocalJSONData, RemoteJSONData
from hknweb.tutoring.scheduler.schedule import schedule


class SchedulerTests(TestCase):
    SEED = 42
    ITERATIONS_MUL = 10
    ALLOWABLE_MARGIN = -15

    TEST_DIR = "media/tutoring-algorithm/test/"
    TEST_URL = (
        "https://raw.githubusercontent.com/compserv/tutoring-algorithm/master/test/"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.can_run_local: bool = os.path.exists(self.TEST_DIR)
        self.can_run_remote: bool = (
            requests.get(f"{self.TEST_URL}exp_results.txt").status_code == 200
        )
        self.assertTrue(
            self.can_run_local or self.can_run_remote,
            "Can't run either local or remote scheduler tests",
        )

    def setUp(self):
        random.seed(self.SEED)

    def _helper_test_scheduler(
        self,
        prev_results_strs: List[str],
        get_data_fn: Callable[[int], Data],
    ):
        # Load target experiment results
        prev_results_strs = prev_results_strs[-8:]
        parse_result = lambda s: (s[:2], int(s[8:11]))
        prev_results = dict(map(parse_result, prev_results_strs))

        # Run experiments
        scores = []
        for i in range(1, 7 + 1):
            data: Data = get_data_fn(i)
            score = schedule(
                data,
                print_output=False,
                weighting_str="old_gardener",
                iterations_mul=self.ITERATIONS_MUL,
            )

            scores.append(score)

        for i, score in enumerate(scores):
            name = f"s{i+1}"
            prev_score = prev_results[name]
            off_by = 100 * (1 - (prev_score / score))
            self.assertGreaterEqual(
                off_by,
                self.ALLOWABLE_MARGIN,
                msg=f"{name}: {prev_score} {int(score)} {off_by}",
            )

    def test_scheduler_url(self):
        if not self.can_run_remote:
            return

        prev_results_strs: List[str] = requests.get(
            f"{self.TEST_URL}exp_results.txt"
        ).content.decode()
        prev_results_strs = list(filter(None, prev_results_strs.split("\n")))
        get_data_fn: Callable[[int], Data] = lambda i: RemoteJSONData(
            f"{self.TEST_URL}s{i}.json"
        )

        self._helper_test_scheduler(prev_results_strs, get_data_fn)

    def test_scheduler_local(self):
        if not self.can_run_local:
            return

        prev_results_strs: List[str] = open(
            f"{self.TEST_DIR}exp_results.txt"
        ).readlines()
        get_data_fn: Callable[[int], Data] = lambda i: LocalJSONData(
            f"{self.TEST_DIR}s{i}.json"
        )

        self._helper_test_scheduler(prev_results_strs, get_data_fn)
