from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages

from .forms import OfficerForm


def index(request):
    form = OfficerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.assignGroups()
            messages.info(request, "New Officers have been added")
            return redirect("/elections")
        else:
            return render(request, "elections/index.html", {"form": OfficerForm(None)})

    return render(request, "elections/index.html", {"form": form})
