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
        context = {}

        status = self.request.POST.get(Attr.STATUS, UploadStages.UPLOAD)
        if status == UploadStages.UPLOAD:
            context = self._present_upload()
        elif status == UploadStages.QUESTIONS:
            context = self._present_questions()
        elif status == UploadStages.INSTRUCTORS:
            context = self._present_instructors()
        elif status == UploadStages.FINISHED:
            context = self._finished()

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
