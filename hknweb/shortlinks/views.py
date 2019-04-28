from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Links

def index(request, temp):
    return HttpResponse("Hello, world. You're at " + temp)

def openLink(request, temp):
    redirectLink = Links.objects.get(name=temp)
    link = redirectLink.redirect
    print(link)
    return redirect(link)
