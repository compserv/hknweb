import csv

from django.http.response import Http404
from django.shortcuts import redirect
from django.contrib import messages

from hknweb.utils import login_and_permission

from hknweb.course_surveys.constants import Attr, COURSE_SURVEYS_EDIT_PERMISSION


@login_and_permission(COURSE_SURVEYS_EDIT_PERMISSION)
def upload_csv(request):
    if request.method != "POST":
        return Http404()
    next_page = request.POST.get("next", "/")

    cs_csv = request.FILES.get(Attr.COURSE_SURVEYS_CSV, None)

    try:
        decoded_cs_csv = cs_csv.read().decode("utf-8").splitlines()
        cs_csv = csv.DictReader(decoded_cs_csv)
    except Exception as e:
        messages.error(request, "Something went wrong with decoding the csv: " + str(e))
        return redirect(next_page)

    # blah blah blah csv stuff

    messages.success(request, "Successfully uploaded CSV!")
    return redirect(next_page)
