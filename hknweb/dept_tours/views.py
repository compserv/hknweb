from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.views.generic.edit import FormView
from datetime import datetime

from .models import DepartmentTourRequest
from .forms import DepartmentTourForm

# Create your views here.
class IndexView(FormView):
    template_name = 'dept_tours/index.html'
    model = DepartmentTourRequest
    form_class = DepartmentTourForm
    success_url = "/dept_tours"

    """
    def get_context_data(self):
    	tour_requests = DepartmentTourRequest.objects.all()
    	form_class = DepartmentTourForm
    	context = {
    		'tour_requests': tour_requests,
    		'form': form_class
    	}
    	return context
    """

    def form_valid(self, form):
    	form.save()
    	msg = "Your request for a department tour has been successfully submitted!\n A copy of your request has been sent" + \
    		" to " + form.instance.email
    	messages.success(self.request, msg)
    	return super().form_valid(form)

