from django.shortcuts import redirect
from django.http import HttpResponse

from .models import Link

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def openLink(request, temp):
    redirectLink = Link.objects.get(name=temp)
    link = redirectLink.redirect
    print(link)
    return redirect(link)

