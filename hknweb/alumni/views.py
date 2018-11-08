from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Alumnus
from .forms import AlumniForm
import operator
from functools import reduce


class IndexView(generic.TemplateView):
    template_name = 'alumni/index.html'


class SearchView(generic.ListView):
    """
    Display an alumni list page filtered by the search query.
    """
    template_name = 'alumni/search.html'
    context_object_name = 'matching_alumni_list'
    paginate_by = 10

    def get_queryset(self):
        result = Alumnus.objects

        query = self.request.GET.get('q')
        if not query:
            return []

        print(query)
        query_list = query.split()
        result = result.filter(
            reduce(operator.and_,
                   (Q(first_name__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(city__icontains=q) for q in query_list))
        )
        print(result)
        return result


def FormView(request):
    form = AlumniForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/alumni/form_success')
        else:
            return render(request, 'alumni/form.html', {'form': form})

    return render(request, 'alumni/form.html', {'form':form})

def FormViewSuccess(request):
    form = AlumniForm(request.POST or None)
    if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('alumni/form_success')
            else:
                return render(request, 'alumni/form.html', {'form':form})
    return render(request, 'alumni/form_success.html', {'form':form})

