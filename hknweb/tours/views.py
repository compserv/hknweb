from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
import datetime
from django.views.generic.edit import FormView
from .forms import *
from django.contrib import messages
from .models import DepTour

def index(request):
    tour = DepTour.objects

    context = {
        'tour': tour,
    }
    return render(request, 'tours/index.html', context)

def tour(request):
    form = TourRequest(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            tour = form.save(commit=False)
            tour.save()
            messages.success(request, 'Your request has been sent!')
            return redirect('/tours/confirm')
        else:
            print(form.errors)
            messages.error(request, 'Something went wrong oops')
            return render(request, 'tours/index.html', {'form': TourRequest(None)})
    return render(request, 'tours/index.html', {'form': TourRequest(None)})

def confirm(request):
    tour = DepTour.objects

    context = {
        'tour': tour,
    }
    return render(request, 'tours/confirm.html', context)
