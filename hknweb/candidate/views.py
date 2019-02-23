from django.views import generic
from django.views.generic.edit import FormView, UpdateView
<<<<<<< HEAD
from django.shortcuts import render, redirect, reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
=======
from django.shortcuts import render, redirect
>>>>>>> parent of 56a99cd... Add email mechanism

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
<<<<<<< HEAD
        self.send_email(form)
        return super().form_valid(form)

    def send_email(self, form):
        subject = 'Confirm Officer Challenge'
        officer_email = form.instance.officer.email
        text_content = 'Confirm officer challenge'

        candidate_name = form.instance.requester.get_full_name()
        candidate_username = form.instance.requester.username
        # host = self.request.get_host()
        link = self.request.build_absolute_uri(
                reverse("candidate:challengeconfirm", kwargs={ 'pk' : form.instance.id }))
        html_content = render_to_string(
            'candidate/email.html',
            {
                'pk': form.instance.id,
                'candidate_name' : candidate_name,
                'candidate_username' : candidate_username,
                'link' : link,
            }
        )
        msg = EmailMultiAlternatives(subject, text_content,
                'no-reply@hkn.eecs.berkeley.edu', [officer_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
=======
        return super().form_valid(form)
>>>>>>> parent of 56a99cd... Add email mechanism

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
