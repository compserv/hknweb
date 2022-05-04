from django.http import Http404, HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import redirect

from hknweb.candidate.forms import BitByteRequestForm


def bitbyte(request):
    if request.method != "POST":
        return Http404()

    form = BitByteRequestForm(request.POST or None)
    if not form.is_valid():
        return HttpResponseBadRequest()

    form.save()
    messages.success(request, "Your bitbyte request was submitted!")
    return redirect("candidate:candidate_portal")
