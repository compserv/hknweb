from django.shortcuts import render
from django.http import HttpResponse


def calendar(request):
    return HttpResponse("Hello, world. You're at the calendar index.")


def future(request):
    return HttpResponse("Hello, world. You're at the future index.")


def past(request):
    return HttpResponse("Hello, world. You're at the past index.")


def rsvps(request):
    return HttpResponse("Hello, world. You're at the rsvps index.")
