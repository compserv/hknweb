from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect


class IndexView(generic.TemplateView):
    template_name = 'alumni/index.html'


# def index(request):
#     context = {
#     }
#     return render(request, 'alumni/index.html', context)

class FormView(generic.TemplateView):
    template_name = 'alumni/form.html'

