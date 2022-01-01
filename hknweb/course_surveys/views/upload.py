import csv

from django.views.generic import TemplateView


from hknweb.utils import method_login_and_permission

from hknweb.course_surveys.constants import (
    Attr,
    UploadStages,
    UploadStageInfo,
)


@method_login_and_permission("course_surveys.change_academicentity")
class UploadView(TemplateView):
    template_name = "course_surveys/upload.html"

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}

        status = self.request.POST.get(Attr.STATUS, UploadStages.UPLOAD)
        if status == UploadStages.UPLOAD:
            context = self._do_upload()
        elif status == UploadStages.QUESTIONS:
            context = self._do_merge_questions()
        elif status == UploadStages.INSTRUCTORS:
            context = self._do_merge_instructors()
        elif status == UploadStages.FINISHED:
            context = self._do_finished()

        return context

    def _do_upload(self):
        cs_csv = self.request.FILES.get(Attr.COURSE_SURVEYS_CSV, None)
        if cs_csv is None:
            return UploadStageInfo.UPLOAD
        else:
            decoded_cs_csv = cs_csv.read().decode("utf-8").splitlines()
            cs_csv = csv.DictReader(decoded_cs_csv)
            return UploadStageInfo.QUESTIONS

    def _do_merge_questions(self):
        return UploadStageInfo.INSTRUCTORS

    def _do_merge_instructors(self):
        return UploadStageInfo.FINISHED

    def _do_finished(self):
        return UploadStageInfo.FINISHED
