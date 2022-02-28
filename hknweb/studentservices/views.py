from django.shortcuts import render

from hknweb.studentservices.forms import DocumentForm


SUBMIT_TEMPLATE = "studentservices/resume_critique_submit.html"
UPLOADED_TEMPLATE = "studentservices/resume_critique_uploaded.html"


def resume_critique_submit(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, UPLOADED_TEMPLATE)
        else:
            form = DocumentForm()
            return render(
                request,
                SUBMIT_TEMPLATE,
                {
                    "form": form,
                    "err": True,
                },
            )

    form = DocumentForm()
    return render(
        request,
        SUBMIT_TEMPLATE,
        {
            "form": form,
            "err": False,
        },
    )


def resume_critique_uploaded(request):
    form = DocumentForm()
    return render(request, SUBMIT_TEMPLATE, {"form": form})
