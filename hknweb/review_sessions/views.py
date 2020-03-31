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
    review_sessions = ReviewSession.objects.order_by('-start_time')

    context = {
        'review_sessions': review_sessions,
    }
    return render(request, 'reviewsessions/index.html', context)
