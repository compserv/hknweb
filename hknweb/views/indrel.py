from django.shortcuts import render

from hknweb.utils import allow_public_access


@allow_public_access
def index(request):
    return render(request, "indrel/index.html")


@allow_public_access
def resume_book(request):
    return render(request, "indrel/resume_book.html")


@allow_public_access
def infosessions(request):
    return render(request, "indrel/infosessions.html")


@allow_public_access
def career_fair(request):
    return render(request, "indrel/career_fair.html")


@allow_public_access
def contact_us(request):
    return render(request, "indrel/contact_us.html")
