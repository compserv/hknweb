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

@allow_public_access
def resume_book(request):
    return render(
        request,
        "industry/resume_book.html",
    )

@allow_public_access
def eecs_career_fair(request):
    return render(
        request,
        "industry/eecs_career_fair.html",
    )

@allow_public_access
def infosessions(request):
    return render(
        request,
        "industry/infosessions.html",
    )

@allow_public_access
def current_sponsors(request):
    return render(
        request,
        "industry/current_sponsors.html",
    )