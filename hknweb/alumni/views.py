from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect

from .forms import AlumniForm


class IndexView(generic.TemplateView):
    template_name = 'alumni/index.html'


def FormView(request):
    form = AlumniForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/alumni/form_success')
        else:
            return render(request, 'alumni/form.html', {'form': form})

    return render(request, 'alumni/form.html', {'form':form})

def FormViewSuccess(request):
    form = AlumniForm(request.POST or None)
    if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('alumni/form_success')
            else:
                return render(request, 'alumni/form.html', {'form':form})
    return render(request, 'alumni/form_success.html', {'form':form})
