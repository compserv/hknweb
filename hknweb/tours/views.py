from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
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

def send_request_email(request, form):
        subject = 'Department Tour Request'
        officer_email = 'conhuang@hkn.mu'

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
        msg = EmailMultiAlternatives(subject, subject,
                'no-reply@hkn.eecs.berkeley.edu', [officer_email])
        msg.attach_alternative(html_content, "text/html")
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
            print(form.errors)
            messages.error(request, 'Something went wrong! Your request did not send. Try again, or email deprel@hkn.eecs.berkeley.edu.')
            return render(request, 'tours/index.html', {'form': TourRequest(None)})
    return render(request, 'tours/index.html', {'form': TourRequest(None)})
