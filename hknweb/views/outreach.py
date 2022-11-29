from django.shortcuts import render

# Create your views here.
from hknweb.utils import allow_public_access


@allow_public_access
def outreach(request):
    return render(request, "outreach.html")
