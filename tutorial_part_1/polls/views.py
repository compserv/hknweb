from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

"""def index(request):
    latest_qs = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_qs': latest_qs,
    }
    return render(request, 'polls/index.html', context)
    
def detail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    context = {
        'q': q
    }
    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    context = {
        'q': q
    }
    return render(request, 'polls/results.html', context)"""

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "latest_qs"

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    context_object_name = "q"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = "q"
    
def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        selected = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'q': q,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected.votes += 1
        selected.save()
    # after successfully handling POST data, redirect so that user data is not posted twice if they hit back
    return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))