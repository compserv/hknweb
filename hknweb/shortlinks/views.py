from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Links

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def openLink(request, temp):
    redirectLink = Links.objects.get(name=temp)
    link = redirectLink.redirect
    print(link)
    return redirect(link)

