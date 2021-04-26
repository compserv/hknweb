from django.shortcuts import render, redirect, reverse

from hknweb.models import Profile
from .forms import SearchResumeForm

def index(request):
    if request.method == 'POST':
        form = SearchResumeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        return redirect(reverse('results', kwargs={'first_name': data['first_name'], 'last_name': data['last_name']}))
    context = {
        'search_form': SearchResumeForm,
    }
    return render(request, 'resumes/index.html', context)

def results(request, first_name, last_name):
    profiles_filtered_first = Profile.objects.filter(user__first_name__contains=first_name)
    profiles_filtered_last = profiles_filtered_first.filter(user__last_name__contains=last_name)
    profiles = profiles_filtered_last.order_by('user')
    context = {
        'profiles': profiles,
    }
    return render(request, 'resumes/results.html', context)