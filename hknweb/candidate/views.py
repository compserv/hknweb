from django.views import generic
from django.views.generic.edit import FormView
from django.shortcuts import render

from .models import OffChallenge
from .forms import ChallengeRequestForm

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'candidate/index.html'


class CandRequestView(FormView, generic.ListView):
    template_name = 'candidate/candreq.html'
    # model = OffChallenge
    # fields = ['name', 'officer', 'description', 'proof']
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

        result = result.order_by('-request_date')
        return result

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
