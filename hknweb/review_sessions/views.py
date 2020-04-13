from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views import generic

from .models import ReviewSession

# views

def index(request):
    reviewsessions = ReviewSession.objects.order_by('-start_time')

    context = {
        'reviewsessions': reviewsessions,
    }
    return render(request, 'reviewsessions/index.html', context)

@permission_required('reviewsessions.add_reviewsession', login_url='/accounts/login/')
def add_reviewsession(request):
    form = ReviewSessionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            reviewsession = form.save(commit=False)
            reviewsession.created_by = request.user
            reviewsession.save()
            messages.success(request, 'Review session has been added!')
            return redirect('/reviewsessions')
        else:
            print(form.errors)
            messages.success(request, 'Something went wrong oops')
            return render(request, 'reviewsessions/reviewsession_add.html', {'form': ReviewSessionForm(None)})
    return render(request, 'reviewsessions/reviewsession_add.html', {'form': ReviewSessionForm(None)})
