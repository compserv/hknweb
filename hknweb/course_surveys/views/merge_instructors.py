import json

from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from hknweb.utils import login_and_permission

from hknweb.academics.models import Instructor
from hknweb.course_surveys.constants import Attr, COURSE_SURVEYS_EDIT_PERMISSION


@login_and_permission(COURSE_SURVEYS_EDIT_PERMISSION)
def merge_instructors(request):
    if request.method != "POST":
        raise Http404()

    instructor_ids = request.GET.get(Attr.INSTRUCTOR_IDS, None)
    instructor_ids = json.loads(instructor_ids)
    instructor_ids = list(map(int, instructor_ids))
    if len(instructor_ids) < 2:
        return HttpResponseBadRequest()

    base_instructor = Instructor.objects.get(pk=instructor_ids[0])
    for id in instructor_ids[1:]:
        instructor = Instructor.objects.get(pk=id)

        for icsr in instructor.icsr_instructor.all():
            icsr.icsr_instructor = base_instructor
            icsr.save()

        instructor.delete()

    return HttpResponse()
