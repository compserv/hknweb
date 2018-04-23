from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse("Hello, world. You're at the people index.")


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
