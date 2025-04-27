from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from hknweb.utils import allow_public_access

@allow_public_access
def what_is_hkn(request):
    return render(
        request,
        "industry/what_is_hkn.html",
    )