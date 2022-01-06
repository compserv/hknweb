from django.views.generic import TemplateView


from hknweb.utils import method_login_and_permission

from hknweb.academics.models import Question, Instructor
from hknweb.course_surveys.constants import (
    Attr,
    COURSE_SURVEYS_EDIT_PERMISSION,
    UploadStages,
    UploadStageInfo,
)


@method_login_and_permission(COURSE_SURVEYS_EDIT_PERMISSION)
class UploadView(TemplateView):
    template_name = "course_surveys/upload.html"

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        current_status = self.request.POST.get(Attr.STATUS, UploadStages.UPLOAD)

        status = current_status
        if self.request.POST.get(Attr.NEXT, None):
            status = self.request.POST.get(Attr.NEXT_STATUS)
        elif self.request.POST.get(Attr.BACK, None):
            status = self.request.POST.get(Attr.PREVIOUS_STATUS)

        status_fn_mapping = {
            UploadStages.UPLOAD: self._present_upload,
            UploadStages.QUESTIONS: self._present_questions,
            UploadStages.INSTRUCTORS: self._present_instructors,
            UploadStages.FINISHED: self._finished,
        }
        fn = status_fn_mapping.get(status, None)
        context = fn() if fn is not None else {}

        return context

    def _present_upload(self):
        return UploadStageInfo.UPLOAD

    def _present_questions(self):
        existing_questions = []
        for q in Question.objects.all():
            most_recent_rating = q.rating_question.latest(
                "rating_survey__survey_icsr__icsr_semester__year",
                "-rating_survey__survey_icsr__icsr_semester__year_section",
            )
            existing_questions.append(
                {
                    Attr.ID: q.id,
                    Attr.TEXT: most_recent_rating.question_text,
                }
            )

        return {
            **UploadStageInfo.QUESTIONS,
            Attr.EXISTING_QUESTIONS: existing_questions,
        }

    def _present_instructors(self):
        existing_instructors = []
        for i in Instructor.objects.all():
            most_recent_icsr = i.icsr_instructor.latest(
                "icsr_semester__year",
                "-icsr_semester__year_section",
            )
            existing_instructors.append(
                {
                    Attr.ID: i.instructor_id,
                    Attr.NAME: "{} {}".format(
                        most_recent_icsr.first_name, most_recent_icsr.last_name
                    ),
                }
            )

        return {
            **UploadStageInfo.INSTRUCTORS,
            Attr.EXISTING_INSTRUCTORS: existing_instructors,
        }

    def _finished(self):
        return UploadStageInfo.FINISHED
