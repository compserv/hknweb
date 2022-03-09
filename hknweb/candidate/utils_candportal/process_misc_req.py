from hknweb.candidate.models import (
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
)


class MiscReqProcessorBase:
    roster_model = None
    completed_roster_model = None
    order_by = None

    all_done_processor = lambda all_done, other_bool: all_done and other_bool
    all_done_initial = True

    title = None
    filter_model_by = None

    @classmethod
    def completed_process(cls, user, required, completed):
        entry = completed.filter(**{cls.filter_model_by: required.id}).first()
        if entry is None:
            return False
        return user in entry.users.all()

    @classmethod
    def process_status(cls, user, candidate_semester):
        requirements = candidate_semester and cls.roster_model.objects.filter(
            visible=True, candidateSemesterActive=candidate_semester.id
        ).order_by(cls.order_by)

        completed_roster = cls.completed_roster_model.objects.all()
        resulting_statuses = []
        all_done = cls.all_done_initial

        if requirements is not None:
            for requirement in requirements:
                is_completed = cls.completed_process(user, requirement, completed_roster)
                all_done = cls.all_done_processor(all_done, is_completed)
                resulting_statuses.append({
                    "requirement": requirement,
                    "status": is_completed,
                })

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
