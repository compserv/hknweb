from django.http import Http404, JsonResponse
from django.shortcuts import render

import csv

from hknweb.thread.models import ThreadTask
from hknweb.utils import login_and_permission

from hknweb.candidate.constants import ATTR
from hknweb.candidate.utils import spawn_threaded_add_cands_and_email


@login_and_permission("auth.add_user")
def create_candidates_view(request):
    """
    View for creating multiple candidates given a CSV of their information
    See "add_cands" for more details
    """
    return render(request, "candidate/create_candidates.html")


@login_and_permission("auth.add_user")
def add_cands(request):
    if request.method != ATTR.POST:
        raise Http404()

    cand_csv_file = request.FILES.get(ATTR.CAND_CSV, None)
    if (cand_csv_file is None):
        return JsonResponse({'success': False, 'id': -1, 'message': "No file detected (can be internal error)"})
    if (not cand_csv_file.name.endswith(ATTR.CSV_ENDING)):
        return JsonResponse({'success': False, 'id': -1, 'message': "Please input a csv file!"})
    decoded_cand_csv_file = cand_csv_file.read().decode(ATTR.UTF8SIG).splitlines()
    cand_csv = csv.DictReader(decoded_cand_csv_file)
    num_rows = sum(1 for _ in csv.DictReader(decoded_cand_csv_file))
    
    website_login_link = request.build_absolute_uri("/accounts/login/")
    task_id = spawn_threaded_add_cands_and_email(cand_csv, website_login_link, num_rows)
    
    return JsonResponse({'success': True, 'id': task_id, 'message': ''})


@login_and_permission("auth.add_user")
def check_mass_candidate_status(request, id):
    task = ThreadTask.objects.get(pk=id)
    return JsonResponse({'progress': task.progress, 'message': task.message,
                         'is_successful': task.is_successful, 'is_done': task.is_done})
