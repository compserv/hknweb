from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect

from .forms import AlumniForm

class IndexView(generic.TemplateView):
    template_name = 'alumni/index.html'


# def index(request):
#     context = {
#     }
#     return render(request, 'alumni/index.html', context)

def FormView(request):
    form = AlumniForm(request.POST or None)
    
    if form.is_valid():
        form.save()

    context = {'form': form}
    return render(request, 'alumni/form.html', context)

