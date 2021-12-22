from django.shortcuts import render
from hknweb.resume.forms import DocumentForm


def index(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "resume/uploaded.html")
        else:
            form = DocumentForm()
            return render(
                request,
                "resume/index.html",
                {
                    "form": form,
                    "err": True,
                },
            )

    form = DocumentForm()
    return render(
        request,
        "resume/index.html",
        {
            "form": form,
            "err": False,
        },
    )


def submitted(request):
    form = DocumentForm()
    return render(request, "resume/index.html", {"form": form})
