from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect


# class IndexView(generic.TemplateView):
#     template_name = 'alumni/index.html'


def index(request):
    context = {
    }
    return render(request, 'alumni/index.html', context)


def form(request):
    return HttpResponse("Hello, world. You're at the form.")
