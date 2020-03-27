from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import TourRequest
from django.contrib import messages
from .models import DepTour

def index(request):
    tour = DepTour.objects

    context = {
        'tour': tour,
    }
    return render(request, 'tours/index.html', context)

def send_request_email(request, form):
        subject = 'Department Tour Request'
        officer_email = 'deprel@hkn.eecs.berkeley.edu'

        html_content = render_to_string(
            'tours/request_email.html',
            {
                'name' : form.instance.name,
                'time' : form.instance.desired_time,
                'date' : form.instance.date,
                'email': form.instance.email,
                'phone': form.instance.phone,
                'comments': form.instance.comments,
            }
        )
        msg = EmailMessage(subject, html_content,
                'no-reply@hkn.eecs.berkeley.edu', [officer_email])
        msg.content_subtype = 'html'
        msg.send()

def tour(request):
    form = TourRequest(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            tour = form.save(commit=False)
            tour.save()
            
            # send_request_email(request, form)

            messages.success(request, 'Your request has been sent!')
            return redirect('/tours/')
        else:
            msg = 'Something went wrong! Your request did not send. Try again, or email deprel@hkn.mu.'
            messages.error(request, msg)
    return render(request, 'tours/index.html', {'form': form})
