from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Links as Link

def index(request, temp):
    return HttpResponse("Hello, world. You're at " + temp)

def openLink(request, temp):
    redirectLink = Link.objects.get(name=temp)
    link = redirectLink.redirect
    print(link)
    return redirect(link)
