import json

from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from hknweb.utils import login_and_permission

from hknweb.academics.models import Question
from hknweb.course_surveys.constants import Attr, COURSE_SURVEYS_EDIT_PERMISSION


@login_and_permission(COURSE_SURVEYS_EDIT_PERMISSION)
def merge_questions(request):
    if request.method != "POST":
        raise Http404()

    question_ids = request.GET.get(Attr.QUESTION_IDS, None)
    question_ids = json.loads(question_ids)
    question_ids = list(map(int, question_ids))
    if len(question_ids) < 2:
        return HttpResponseBadRequest()

    base_question = Question.objects.get(pk=question_ids[0])
    for id in question_ids[1:]:
        question = Question.objects.get(pk=id)

        for rating in question.rating_question.all():
            rating.rating_question = base_question
            rating.save()

        question.delete()

    return HttpResponse()
