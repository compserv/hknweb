from django.views import generic
from django.views.generic.edit import CreateView

from .models import OffChallenge

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'candidate/index.html'

class CandRequestView(CreateView):
    template_name = 'candidate/candreq.html'
    model = OffChallenge
    fields = ['name', 'officer', 'description', 'proof']
    success_url = "/cand/candreq"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.requester = self.request.user
        return super().form_valid(form)
