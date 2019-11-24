from django.shortcuts import render
from django.views import generic
import datetime
from django.views.generic.edit import FormView
from .forms import TourRequest

class DepTourView(FormView):
    template_name = 'tours/index.html'
    form_class = TourRequest

    # def add_event(request):
    #     form = TourRequest(request.POST or None)
    #     if request.method == 'POST':
    #         if form.is_valid():
    #             event = form.save(commit=False)
    #             event.created_by = request.user
    #             event.save()
    #             messages.success(request, 'Tour has been requested!')
    #             return redirect('/events')
    #         else:
    #             print(form.errors)
    #             messages.success(request, 'Something went wrong oops')
    #             return render(request, 'events/add_event.html', {'form': EventForm(None)})
    #     return render(request, 'events/add_event.html', {'form': EventForm(None)})

    # def get(self, request):
    #     form = TourRequest()
    #     return render(request, self.template_name, {'form': form})
    #
    # def post(self, request):
    #     form = TourRequest(request.POST)
    #     if form.is_valid():
    #         name = form.cleaned_data("name")
