from django.http import Http404, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User

from hknweb.utils import login_and_access_level, GROUP_TO_ACCESSLEVEL

from hknweb.candidate.models import OffChallenge, BitByteActivity, Logistics


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def confirm_challenge(request, pk: int, action: int):
    if request.method != "POST":
        raise Http404()

    offchallenge = get_object_or_404(OffChallenge, pk=pk)
    offchallenge.officer_confirmed = action == 0  # 0 means confirmed
    offchallenge.save()

    return redirect("candidate:officer_portal")


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def confirm_bitbyte(request, pk: int, action: int):
    if request.method != "POST":
        raise Http404()

    bitbyte = get_object_or_404(BitByteActivity, pk=pk)
    bitbyte.confirmed = action == 0
    bitbyte.save()

    return redirect("candidate:officer_portal")


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def confirm_bitbyte(request, pk: int, action: int):
    if request.method != "POST":
        raise Http404()

    bitbyte = get_object_or_404(BitByteActivity, pk=pk)
    bitbyte.confirmed = action == 0
    bitbyte.save()

    return redirect("candidate:officer_portal")


@login_and_access_level(GROUP_TO_ACCESSLEVEL["officer"])
def checkoff_req(request):
    if request.method != "POST":
        raise Http404()

    logistics_id = request.POST.get("logistics_id", None)
    type = request.POST.get("type", None)
    obj_title = request.POST.get("obj_title", None)
    user_id = request.POST.get("user_id", None)
    operation = request.POST.get("operation", None)

    logistics: Logistics = Logistics.objects.get(pk=logistics_id)
    if not logistics:
        return HttpResponseBadRequest()

    objs = None
    if type == "form_req":
        objs = logistics.form_reqs
    elif type == "misc_req":
        objs = logistics.misc_reqs

    obj = objs.get(title=obj_title)
    user = User.objects.get(pk=user_id)
    try:
        operation: int = int(operation)
    except ValueError:
        operation = None

    if not (objs or obj or user) or operation not in [0, 1]:
        return HttpResponseBadRequest()

    if operation == 0:  # confirm
        obj.completed.add(user)
    elif operation == 1:  # unconfirm
        obj.completed.remove(user)
    obj.save()

    return HttpResponse()
