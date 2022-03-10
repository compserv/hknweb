import csv
from collections import OrderedDict
import threading
import time
from typing import Tuple

from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, Group, User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from hknweb.thread.models import ThreadTask
from hknweb.utils import login_and_permission, get_rand_photo
from hknweb.models import Profile
from hknweb.views.users import get_current_cand_semester

from hknweb.candidate.constants import (
    ATTR,
    CandidateDTO,
    DEFAULT_RANDOM_PASSWORD_LENGTH,
)


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
    if cand_csv_file is None:
        return JsonResponse(
            {
                "success": False,
                "id": -1,
                "message": "No file detected (can be internal error)",
            }
        )
    if not cand_csv_file.name.endswith(ATTR.CSV_ENDING):
        return JsonResponse(
            {"success": False, "id": -1, "message": "Please input a csv file!"}
        )
    decoded_cand_csv_file = cand_csv_file.read().decode(ATTR.UTF8SIG).splitlines()
    cand_csv = csv.DictReader(decoded_cand_csv_file)
    num_rows = sum(1 for _ in csv.DictReader(decoded_cand_csv_file))

    website_login_link = request.build_absolute_uri("/accounts/login/")
    task_id = spawn_threaded_add_cands_and_email(cand_csv, website_login_link, num_rows)

    return JsonResponse({"success": True, "id": task_id, "message": ""})


@login_and_permission("auth.add_user")
def check_mass_candidate_status(request, id):
    task = ThreadTask.objects.get(pk=id)
    return JsonResponse(
        {
            "progress": task.progress,
            "message": task.message,
            "is_successful": task.is_successful,
            "is_done": task.is_done,
        }
    )


NO_ACTION_PLS_FIX = "No candidate account actions have been taken, so re-upload the entire file after fixing the errors."


def spawn_threaded_add_cands_and_email(cand_csv, website_login_link, num_rows):
    """
    Spawn a single background thread to provision candidate

    """
    task = ThreadTask()
    task.save()
    t = threading.Thread(
        target=threaded_add_cands_and_email,
        args=[cand_csv, num_rows, website_login_link, task],
    )
    task.startThread(t)
    return task.id


def threaded_add_cands_and_email(cand_csv, num_rows, website_login_link, task):
    try:
        result, msg = add_cands_and_email(cand_csv, num_rows, website_login_link, task)
    except Exception as e:
        result = False
        msg = str(e)
    task.message = msg
    if result:
        task.complete()
    else:
        task.failure()
    task.progress = 100
    task.save()


def check_duplicates(
    candidatedto: CandidateDTO,
    row: OrderedDict,
    email_set: set,
    username_set: set,
    i: int,
) -> Tuple[bool, str]:
    error_msg = ""
    # Check for duplicate Email
    cand_email_in_set = candidatedto.email in email_set
    if cand_email_in_set or User.objects.filter(email=candidatedto.email).count() > 0:
        if cand_email_in_set:
            error_msg = "Duplicate email {} in the Candidate data.".format(
                candidatedto.email
            )
        else:
            error_msg = "Account with email {} already exists.".format(
                candidatedto.email
            )
        error_msg += " "
        error_msg += "No candidate account actions have been taken, so re-upload the entire file after fixing the errors."
        error_msg += " "
        error_msg += "Error Row Information at row {}: {}.".format(i + 1, row)
        return True, error_msg
    # Check for duplicate Username
    cand_username_in_set = candidatedto.username in username_set
    if (
        cand_username_in_set
        or User.objects.filter(username=candidatedto.username).count() > 0
    ):
        if cand_username_in_set:
            error_msg = "Duplicate username {} in the Candidate data.".format(
                candidatedto.username
            )
        else:
            error_msg = "Account of username {} already exists.".format(
                candidatedto.username
            )
        error_msg += " "
        error_msg += "No candidate account actions have been taken, so re-upload the entire file after fixing the errors."
        error_msg += " "
        error_msg += "Error Row Information at row {}: {}.".format(i + 1, row)
        return True, error_msg
    return False, ""


def add_cands_and_email(cand_csv, num_rows, website_login_link, task=None):
    candidate_group = Group.objects.get(name=ATTR.CANDIDATE)
    progress_float = 0.0
    CAND_ACC_WEIGHT = 0.75
    EMAIL_WEIGHT = 0.25

    # Sanity check progress
    if task is not None:
        task.progress = 1.0
        task.save()

    # Pre-screen and validate data
    new_cand_list = []
    email_set = set()
    username_set = set()
    current_cand_semester = get_current_cand_semester()
    email_passwords = {}
    if current_cand_semester is None:
        error_msg = "Inform CompServ the following: Please add the current semester in CourseSemester."
        error_msg += " "
        error_msg += NO_ACTION_PLS_FIX
        return False, error_msg

    for i, row in enumerate(cand_csv):
        try:
            candidatedto = CandidateDTO(row)
        except AssertionError as e:
            error_msg = "Invalid CSV format. Check that your columns are correctly labeled, there are NO blank rows, and filled out for each row."
            error_msg += " "
            error_msg += NO_ACTION_PLS_FIX
            error_msg += " "
            error_msg += "Candidate error message: {}.".format(e)
            error_msg += " "
            error_msg += "Row Information at row {}: {}.".format(i + 1, row)
            return False, error_msg

        password = BaseUserManager.make_random_password(
            None, length=DEFAULT_RANDOM_PASSWORD_LENGTH
        )

        duplicate, error_msg = check_duplicates(
            candidatedto, row, email_set, username_set, i
        )
        if duplicate:
            return False, error_msg

        new_cand = User(
            username=candidatedto.username,
            email=candidatedto.email,
        )
        email_set.add(candidatedto.email)
        username_set.add(candidatedto.username)
        new_cand.first_name = candidatedto.first_name
        new_cand.last_name = candidatedto.last_name
        new_cand.set_password(password)
        new_cand_list.append(new_cand)
        email_passwords[new_cand.email] = password

        progress_float = CAND_ACC_WEIGHT * 100 * (i + 1) / num_rows
        if task is not None:
            task.progress = round(progress_float)
            task.save()

    # Reset to CAND_ACC_WEIGHT in case floating point errors
    progress_float = CAND_ACC_WEIGHT * 100
    if task is not None:
        task.progress = round(progress_float)
        task.save()

    num_of_accounts = len(email_set)

    if num_of_accounts != num_rows:
        error_msg = (
            "Internal Error: number of accounts ({}) != number of rows ({})".format(
                num_of_accounts, num_rows
            )
        )
        error_msg += " "
        error_msg += NO_ACTION_PLS_FIX
        return False, error_msg

    # Release the memory once done
    del email_set
    del username_set

    email_errors = []
    for i, new_cand in enumerate(new_cand_list):
        if i != 0 and i % 50 == 0:
            time.sleep(10)
        new_cand.save()
        candidate_group.user_set.add(new_cand)

        profile = Profile.objects.get(user=new_cand)
        profile.candidate_semester = current_cand_semester
        profile.save()

        subject = "[HKN] Candidate account"
        html_content = render_to_string(
            "candidate/new_candidate_account_email.html",
            {
                "subject": subject,
                "first_name": new_cand.first_name,
                "username": new_cand.username,
                "password": email_passwords[new_cand.email],
                "website_link": website_login_link,
                "img_link": get_rand_photo(),
            },
        )
        if settings.DEBUG:
            print("\n")
            print(new_cand.first_name, new_cand.username, new_cand.email)
            print(html_content)
            print("\n")
        else:
            msg = EmailMultiAlternatives(
                subject, subject, settings.NO_REPLY_EMAIL, [new_cand.email]
            )
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except Exception as e:
                email_errors.append((new_cand_list[i].email, str(e)))

        progress_float = (CAND_ACC_WEIGHT * 100) + (
            EMAIL_WEIGHT * 100 * (i + 1) / num_of_accounts
        )
        if task is not None:
            task.progress = round(progress_float)
            task.save()

    # If gone through everything and no errors
    if len(email_errors) > 0:
        error_msg = (
            "An error occured during the sending of emails. "
            + "Candidate Email and Error Messages: "
            + str(email_errors)
            + " --- "
            + "Inform CompServ of the errors, and inform the candidates "
            + "to access their accounts by resetting their password "
            + 'using "Forget your password?" in the Login page. '
            + "All {} candidates added!".format(num_of_accounts)
        )
        return False, error_msg
    else:
        return True, "Successfully added {} candidates!".format(num_of_accounts)
