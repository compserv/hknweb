from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views import generic

from hknweb.utils import login_and_permission, method_login_and_permission
from .models import ReviewSession
from .forms import ReviewSessionForm

# views

def index(request):
    reviewsessions = ReviewSession.objects.order_by('-start_time')

    context = {
        'reviewsessions': reviewsessions,
    }
    return render(request, 'reviewsessions/index.html', context)

@login_and_permission('reviewsessions.view_reviewsession')
def show_details(request, id):
    reviewsession = get_object_or_404(ReviewSession, pk=id)

    context = {
        'reviewsession': reviewsession,
        'can_edit': request.user.has_perm('reviewsessions.change_review_session')
    }
    return render(request, 'reviewsessions/show_details.html', context)

@login_and_permission('reviewsessions.add_reviewsession')
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

@method_login_and_permission('reviewsessions.change_review_session')
class ReviewSessionUpdateView(generic.edit.UpdateView):
    model = ReviewSession
    fields = ['name', 'slug', 'start_time', 'end_time', 'location', 'description']
    template_name_suffix = '_edit'
