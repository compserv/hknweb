from django.views import generic
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import render, redirect

from .models import OffChallenge
from .forms import ChallengeRequestForm, ChallengeConfirmationForm

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'candidate/index.html'


class CandRequestView(FormView, generic.ListView):
    template_name = 'candidate/candreq.html'
    form_class = ChallengeRequestForm
    success_url = "/cand/candreq"

    context_object_name = 'challenge_list'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.requester = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CandRequestView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        result = OffChallenge.objects

        result = result.order_by('-request_date').filter(requester=self.request.user)
        return result


class OfficerConfirmView(FormView):
    template_name = 'candidate/challenge_confirm.html'
    form_class = ChallengeConfirmationForm
    success_url = "/cand/dummy"

    def form_valid(self, form):
        form.instance = OffChallenge.objects.get(id=self.kwargs['pk'])
        form.instance.reviewed = True
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        challenge = OffChallenge.objects.get(id=self.kwargs['pk'])

        context = super(OfficerConfirmView, self).get_context_data(**kwargs)
        context = {
            'challenge' : challenge,
        }
        return context

    # def get_queryset(self):
    #     result = OffChallenge.objects
    #
    #     result = result.order_by('-request_date').filter(requester=self.request.user)
    #     return result


def officer_confirm_view(request, pk):
    challenge = OffChallenge.objects.get(id=pk)
    requester_name = challenge.requester.get_full_name()
    form = ChallengeConfirmationForm(request.POST or None, instance=challenge)
    context = {
        'challenge' : challenge,
        'requester_name' : requester_name,
        'form': form,
    }

    if form.is_valid():
        form.instance.reviewed = True
        form.save()
        return redirect('/cand/dummy')
    return render(request, "candidate/challenge_confirm.html", context=context)


def challenge_detail_view(request, pk):
    challenge = OffChallenge.objects.get(id=pk)
    officer_name = challenge.officer.get_full_name()
    requester_name = challenge.requester.get_full_name()
    context = {
        "challenge" : challenge,
        "officer_name" : officer_name,
        "requester_name" : requester_name,
    }
    return render(request, "candidate/challenge_detail.html", context=context)
