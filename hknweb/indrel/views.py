from django.shortcuts import render


def index(request):
    return render(request, "indrel/index.html")


def resume_book(request):
    return render(request, "indrel/resume_book.html")


def infosessions(request):
    return render(request, "indrel/infosessions.html")


def career_fair(request):
    return render(request, "indrel/career_fair.html")


def contact_us(request):
    return render(request, "indrel/contact_us.html")
