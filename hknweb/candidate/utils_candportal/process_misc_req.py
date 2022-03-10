from typing import Callable
from django.contrib.auth.models import User
from django.db.models import Model, QuerySet

from hknweb.coursesemester.models import Semester

from hknweb.candidate.models import (
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
)


class MiscReqProcessorBase:
    roster_model: Model = None
    completed_roster_model: Model = None
    order_by: str = None

    all_done_processor: Callable = lambda all_done, other_bool: all_done and other_bool
    all_done_initial: bool = True

    title: str = None
    filter_model_by: str = None

    @classmethod
    def completed_process(
        cls, user: User, required: Model, completed: QuerySet
    ) -> bool:
        entry = completed.filter(**{cls.filter_model_by: required.id}).first()
        if entry is None:
            return False
        return user in entry.users.all()

    @classmethod
    def process_status(cls, user: User, candidate_semester: Semester) -> dict:
        requirements = candidate_semester and cls.roster_model.objects.filter(
            visible=True, candidateSemesterActive=candidate_semester.id
        ).order_by(cls.order_by)

        completed_roster = cls.completed_roster_model.objects.all()
        resulting_statuses = []
        all_done = cls.all_done_initial

        if requirements is not None:
            for requirement in requirements:
                is_completed = cls.completed_process(
                    user, requirement, completed_roster
                )
                all_done = cls.all_done_processor(all_done, is_completed)
                resulting_statuses.append(
                    {
                        "requirement": requirement,
                        "status": is_completed,
                    }
                )

        return {
            "title": cls.title,
            "resulting_statuses": resulting_statuses,
            "all_done": all_done,
        }


class CandidateFormProcessor(MiscReqProcessorBase):
    roster_model = CandidateForm
    completed_roster_model = CandidateFormDoneEntry
    order_by = "duedate"

    title = "Complete all required forms"

    filter_model_by = "form"


class DuePaymentProjectProcessor(MiscReqProcessorBase):
    roster_model = DuePayment
    completed_roster_model = DuePaymentPaidEntry
    order_by = "duedate"

    title = "Pay dues"

    filter_model_by = "duePayment"


class CommitteeProjectProcessor(MiscReqProcessorBase):
    roster_model = CommitteeProject
    completed_roster_model = CommitteeProjectDoneEntry
    order_by = "name"

    all_done_processor = lambda all_done, other_bool: all_done or other_bool
    all_done_initial = False

    title = "Complete a Committee Project"

    filter_model_by = "committeeProject"
