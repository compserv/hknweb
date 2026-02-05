from django.shortcuts import render, get_object_or_404, redirect
from hknweb.utils import login_and_committee
from hknweb.tutoring.models import CribSheet, CourseDescription
from hknweb.tutoring.forms import AddCribForm
from hknweb.models import DriveFolderID
from hknweb.coursesemester.models import Semester
from django.conf import settings
from hknweb.google_drive_utils import (
    create_pdf,
    create_folder,
    create_permission,
    delete_permission,
)
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator


@method_decorator(login_and_committee(settings.TUTORING_GROUP), name="dispatch")
class CribView(View):
    template = "tutoring/crib.html"
    paginate_by = 10

    def get_queryset(self, request):
        qs = CribSheet.objects.all()

        q = request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(course__title__icontains=q)
                | Q(title__icontains=q)
                | Q(semester__semester__icontains=q)
                | Q(semester__year__icontains=q)
            )

        course_query = request.GET.get("course", "").strip()
        if course_query:
            qs = qs.filter(course__title=course_query)

        semester_query = request.GET.get("semester", "").strip()
        if semester_query:
            semester_semester, semester_year = semester_query.split()
            qs = qs.filter(
                semester__semester=semester_semester, semester__year=semester_year
            )

        return qs.order_by("-upload_date")

    def get_context(self, request, qs):
        paginator = Paginator(qs, self.paginate_by)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "sheets": page_obj.object_list,
            "semesters": Semester.objects.all().order_by("-year", "-semester"),
            "courses": CourseDescription.objects.all(),
            "form": AddCribForm(),
        }

        return context

    def get(self, request):
        qs = self.get_queryset(request)
        context = self.get_context(request, qs)
        return render(request, self.template, context=context)

    def post(self, request):
        form = AddCribForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            course = form.cleaned_data["course"]
            title = form.cleaned_data["title"]
            comment = form.cleaned_data["comment"]
            semester = Semester.get_current_semester()

            folderID = course.folderID
            if not folderID:
                parent_folderID = DriveFolderID.objects.get(
                    title="Crib Sheets"
                ).folderID
                folder_name = f"{course.title}"
                result = create_folder(folder_name, parents=[parent_folderID])
                if result["status"]:
                    folderID = result["result"]
                    course.folderID = folderID
                    course.save()
                else:
                    return

            result = create_pdf(title, file, parents=[folderID], description=comment)

            if result["status"]:
                sheet = CribSheet.objects.create(
                    semester=semester,
                    course=course,
                    fileID=result["result"],
                    title=title,
                    comment=comment,
                )
                sheet.save()

        qs = self.get_queryset(request)
        context = self.get_context(request, qs)

        return render(request, self.template, context=context)


@login_and_committee(settings.TUTORING_GROUP)
def toggle_public(request, pk):
    sheet = get_object_or_404(CribSheet, pk=pk)
    sheet.public = not sheet.public
    sheet.save()

    if sheet.public:
        create_permission(sheet.fileID, typeID="anyone", role="reader")
    else:
        delete_permission(sheet.fileID, typeID="anyone", role="reader")

    return redirect(request.POST.get("next", "/"))
