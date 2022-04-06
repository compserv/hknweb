import urllib
import json
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from hknweb.forms import (
    ProfileForm,
    SignupForm,
    ValidPasswordForm,
    UpdatePasswordForm,
)
from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings
from hknweb.models import Profile
from hknweb.coursesemester.models import Semester
from hknweb.utils import allow_all_logged_in_users, allow_public_access
import datetime


# context processor for base to know whether a user is in the officer group
def add_officer_context(request):
    return {
        "viewer_is_an_officer": request.user.groups.filter(
            name=settings.OFFICER_GROUP
        ).exists()
    }


def add_exec_context(request):
    return {
        "viewer_is_an_exec": request.user.groups.filter(
            name=settings.EXEC_GROUP
        ).exists()
    }


def get_current_cand_semester():  # pragma: no cover
    # The "first" function will put a "None" for me if semester not created yet
    now = datetime.datetime.now()
    sem = ""
    month = now.month
    if (1 <= month) and (month <= 5):
        sem = "Spring"
    elif (6 <= month) and (month < 8):
        sem = "Summer"
    elif (8 <= month) and (month <= 12):
        sem = "Fall"
    # The "first" function will put a "None" for me if semester not created yet
    return Semester.objects.filter(semester=sem, year=now.year).first()


# views
@allow_public_access
def account_create(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if confirm_recaptcha(request):
                form.save()
            else:  # pragma: no cover
                messages.warning(request, "Invalid reCAPTCHA. Please try again.")
                return render(request, "account/signup.html", {"form": form})
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            profile = Profile.objects.get(user=user)
            profile.candidate_semester = get_current_cand_semester()
            profile.save()

            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "account/signup.html", {"form": form})


def confirm_recaptcha(request):  # pragma: no cover
    if settings.DEBUG:
        return True
    recaptcha_response = request.POST.get("g-recaptcha-response")
    url = "https://www.google.com/recaptcha/api/siteverify"
    values = {"secret": settings.RECAPTCHA_PRIVATE_KEY, "response": recaptcha_response}
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result["success"]


@allow_all_logged_in_users
def account_settings(request):
    current_user = request.user
    if request.method == "POST":
        password_form = UpdatePasswordForm(current_user, request.POST)
        profile_form = ProfileForm(request.POST, instance=current_user.profile)
        verify_form = ValidPasswordForm(request.POST, instance=current_user.profile)
        if verify_form.is_valid():
            correct_password = request.user.check_password(
                verify_form.data.get("password")
            )
            if correct_password:
                if "change_password" in request.POST:
                    if password_form.is_valid():
                        if password_form.has_changed():
                            current_user = password_form.save()
                            update_session_auth_hash(request, current_user)
                            messages.success(
                                request, ("Your password was successfully updated!")
                            )
                    else:
                        messages.error(
                            request,
                            (
                                "Please correct the errors in your Password: {}".format(
                                    list(password_form.errors.values())
                                )
                            ),
                        )
                elif "edit_profile" in request.POST:
                    if profile_form.is_valid():
                        if profile_form.has_changed():
                            # user_form.save()
                            profile = profile_form.save(commit=False)
                            profile.user = request.user
                            profile.save()
                            # user = password_form.save()
                            update_session_auth_hash(request, current_user)
                            messages.success(
                                request, ("Your profile was successfully updated!")
                            )
                    else:
                        messages.error(
                            request,
                            (
                                "Please correct the errors in your Profile data: {}".format(
                                    list(profile_form.errors.values())
                                )
                            ),
                        )
                else:
                    messages.error(request, ("Error: Unknown Submission Action"))
            else:
                messages.error(
                    request, ("Wrong Password. Please enter your current password.")
                )
        else:
            messages.error(
                request,
                (
                    "Please correct the errors in your Current Password: {}".format(
                        list(verify_form.errors.values())
                    )
                ),
            )
        return HttpResponseRedirect(request.path_info)
    else:
        # user_form = SettingsForm(instance = current_user)
        password_form = UpdatePasswordForm(current_user)
        profile_form = ProfileForm(instance=current_user.profile)
        verify_form = ValidPasswordForm(instance=current_user)
        # context = {"user": current_user, 'user_form': user_form, 'password_form': password_form, 'profile_form': profile_form}
        context = {
            "password_form": password_form,
            "profile_form": profile_form,
            "verify_form": verify_form,
        }
        return render(request, "account/settings.html", context=context)
