from django.shortcuts import render
from hknweb.utils import login_and_committee
from hknweb.tutoring.models import CribSheet
from hknweb.tutoring.forms import AddCribForm
from hknweb.coursesemester.models import Semester
from django.conf import settings


@login_and_committee(settings.TUTORING_GROUP)
def crib(request):
    if request.method == "POST":
        curr_semester = Semester.get_current_semester()
        form = AddCribForm(request.POST)
        if form.is_valid():
            new_sheet = form.save(commit=False)
            new_sheet.semester = curr_semester
            new_sheet.save()
    crib = CribSheet.objects.all().order_by("-update_date")

    context = {
        "form": AddCribForm(),
        "crib": crib,
    }

    return render(request, "tutoring/crib.html", context=context)
