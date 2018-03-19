from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

# from .models import Event

def index(request):
    # events = Event.objects.order_by('-created_at')[:10]

    # context = {
    #     'events': events,
    # }
    return render(request, 'events/index.html', context)


def officers(request):
    return HttpResponse("Hello, world. You're at the officers index.")


def committee_members(request):
	return HttpResponse("Hello, world. You're at the committee members index.")


def members(request):
    return HttpResponse("Hello, world. You're at the members index.")

def candidates(request):
    return HttpResponse("Hello, world. You're at the candidates index.")


def election(request):
    return HttpResponse("Hello, world. You're at the election index.")


def contact(request):
    return HttpResponse("Hello, world. You're at the contact index.")
