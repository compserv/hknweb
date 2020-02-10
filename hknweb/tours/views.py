from django.shortcuts import render
from django.views import generic
import datetime
from django.views.generic.edit import FormView
from .forms import *
from .models import DepTour

class IndexView(FormView):
    template_name = 'tours/index.html'
    form_class = TourRequest
    model = DepTour
    success_url = '/confirmedtour/'

    def form_valid(self, form):
        form.instance.requester = self.request.user
        form.save()
        self.send_request_email(form)
        messages.success(self.request, 'Your request has been confirmed!')
        return super().form_valid(form)

class ConfirmView(FormView):
    template_name = 'tours/confirmtour.html'
    form_class = TourConfirmationForm
    model = DepTour
    success_url = '/confirmedtour/'

    def form_valid(self, request):
        form = TourRequest(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                tour = form.save(commit=False)
                tour.created_by = request.user
                tour.save()
                messages.success(request, 'Tour has been requested!')
                return super().form_valid(request)
            else:
                print(form.errors)
                messages.success(request, 'Something went wrong oops')
                return render(request, 'events/add_event.html', {'form': EventForm(None)})
        return render(request, 'events/add_event.html', {'form': EventForm(None)})
