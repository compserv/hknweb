from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404

from .models import Link


def index(request, temp):
    return HttpResponse("Hello, world. You're at " + temp)


def openLink(request, temp):
    count = Link.objects.filter(active=True, name=temp).count()
    if count == 0:
        return render(request, './404.html')
    redirectLink = Link.objects.filter(active=True).get(name=temp)    
    link = redirectLink.redirect
    return redirect(link)
