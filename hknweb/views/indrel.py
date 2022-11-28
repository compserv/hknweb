from django.shortcuts import render

from hknweb.utils import allow_public_access


@allow_public_access
def indrel(request):
    return render(request, "indrel.html")
