from django.views import generic
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import render, redirect, reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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
        self.send_email(form)
        return super().form_valid(form)

    def send_email(self, form):
        subject = 'Confirm Officer Challenge'
        officer_email = form.instance.officer.email
        text_content = 'Confirm officer challenge'

        candidate_name = form.instance.requester.get_full_name()
        candidate_username = form.instance.requester.username
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

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise RuntimeError('User not logged in')
        result = OffChallenge.objects \
                .order_by('-request_date') \
                .filter(requester__exact=self.request.user)
        return result


class OffRequestView(generic.ListView):
    template_name = 'candidate/offreq.html'

    context_object_name = 'challenge_list'

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise RuntimeError('User not logged in')
        result = OffChallenge.objects \
                .order_by('-request_date') \
                .filter(officer__exact=self.request.user)
        return result


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
        return redirect('/cand/reviewconfirm/' + pk)
    return render(request, "candidate/challenge_confirm.html", context=context)


# the page displayed after officer reviews challenge and clicks "submit"
def officer_review_confirmation(request, pk):
    challenge = OffChallenge.objects.get(id=pk)
    requester_name = challenge.requester.get_full_name()
    context = {
        'challenge' : challenge,
        'requester_name' : requester_name,
    }
    return render(request, "candidate/review_confirm.html", context=context)


def challenge_detail_view(request, pk):
    challenge = OffChallenge.objects.get(id=pk)
    officer_name = challenge.officer.get_full_name()
    requester_name = challenge.requester.get_full_name()
    # check whether the view of page is the officer who gave the challenge
    if request.user.is_anonymous:
        raise RuntimeError('User not logged in')
    viewer_is_officer = challenge.officer == request.user
    if viewer_is_officer:
        review_link = request.build_absolute_uri(
                reverse("candidate:challengeconfirm", kwargs={ 'pk' : pk }))
    else:
        review_link = None
    context = {
        "challenge" : challenge,
        "officer_name" : officer_name,
        "requester_name" : requester_name,
        "viewer_is_officer" : viewer_is_officer,
        "review_link" : review_link,
    }
    return render(request, "candidate/challenge_detail.html", context=context)
