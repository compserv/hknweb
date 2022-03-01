from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "serv/index.html")


def eecsday(request):
    return render(request, "serv/eecs_day.html")


def jreecs(request):
    return render(request, "serv/jr_eecs.html")


def bearhacks(request):
    return render(request, "serv/bearhacks.html")


def maker(request):
    return render(request, "serv/maker_shops.html")


def calday(request):
    return render(request, "serv/calday.html")
