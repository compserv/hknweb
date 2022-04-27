from django.shortcuts import render

# Create your views here.
from hknweb.utils import allow_public_access


@allow_public_access
def index(request):
    return render(request, "serv/index.html")


@allow_public_access
def eecsday(request):
    return render(request, "serv/eecs_day.html")


@allow_public_access
def jreecs(request):
    return render(request, "serv/jr_eecs.html")


@allow_public_access
def bearhacks(request):
    return render(request, "serv/bearhacks.html")


@allow_public_access
def maker(request):
    return render(request, "serv/maker_shops.html")


@allow_public_access
def calday(request):
    return render(request, "serv/calday.html")
