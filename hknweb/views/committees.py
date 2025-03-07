from hknweb.utils import allow_public_access
from django.shortcuts import render


@allow_public_access
def portal(request):
    return render(request, "committees.html")

