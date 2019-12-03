from django.shortcuts import render, redirect
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

    def form_valid(self, form):
    	form.save()
    	msg = "Your request for a department tour has been successfully submitted!\n A copy of your request has been sent" + \
    		" to " + form.instance.email
    	messages.success(self.request, msg)
    	form_id = form.instance.id
    	return redirect('/dept_tours/request/{}'.format(form_id))

def request_submitted(request, pk):
	req = DepartmentTourRequest.objects.get(id=pk)
	context = {
		'tour_request': req
	}
	return render(request, 'dept_tours/request_confirm.html', context = context)