from django.shortcuts import render
from django.views import generic
from django.core.mail import EmailMessage
from .models import ResumeBookOrderForm, InfosessionRegistration,IndrelMailer

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
def mailer(request):

    msg = EmailMessage("indrelmailer@gmail.com", "indrelmailer@gmail.com", "indrelmailer@gmail.com",
                       ["indrelmailer@gmail.com"])
    msg.content_subtype="html"
    msg.send()
class MailerView(generic.FormView):
    form_class = IndrelMailer
    template_name = 'indrel/mailer.html'
    success_url="thanks"
    def form_valid(self,form):
        form.send_email(self.request.FILES['template'],self.request.FILES['fill_ins'])
        return super().form_valid(form)