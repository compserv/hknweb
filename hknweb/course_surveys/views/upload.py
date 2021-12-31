from django.views.generic import TemplateView


from hknweb.utils import method_login_and_permission

from hknweb.course_surveys.constants import (
    Attr,
)


@method_login_and_permission("course_surveys.change_academicentity")
class UploadView(TemplateView):
    template_name = "course_surveys/upload.html"
