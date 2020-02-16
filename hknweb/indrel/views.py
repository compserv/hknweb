from django.shortcuts import render
from django.views import generic
from .models import ResumeBookOrderForm, InfosessionRegistration

def index(request):
    return render(request, 'indrel/index.html')

def resume_book(request):
    return render(request, 'indrel/resume_book.html')

def infosessions(request):
    return render(request, 'indrel/infosessions.html')

def career_fair(request):
    return render(request, 'indrel/career_fair.html')

def contact_us(request):
    return render(request, 'indrel/contact_us.html')

class ResumeBookOrderFormView(generic.DetailView):
    model = ResumeBookOrderForm
    template_name = 'indrel/resume_book_order_form.html'

class InfosessionRegistrationView(generic.DetailView):
    model = InfosessionRegistration
    template_name = 'indrel/infosessions_registration.html'

def order_resume_book(request):
    pass

def register_info_session(request):
    pass