from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse
from hknweb.models import *
import ast
from django.contrib.auth.models import User
from hknweb.forms import SettingsForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def account_settings(request):
    current_user = request.user
    if request.method == 'POST':
        user_form = SettingsForm(request.POST, instance = current_user)
        password_form = PasswordChangeForm(current_user, request.POST)
        profile_form = ProfileForm(request.POST, instance = current_user.profile)
        user_form.is_valid()
        correct_password = authenticate(username=request.POST[username], password=user_form.cleaned_data[password])
        if not correct_user:
            messages.error(request, _('Incorrect password. You must enter your password to save changes.'))
        elif user_form.is_valid() and profile_form.is_valid() and password_form.is_valid():
            user_form.save()
            profile_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('/account_settings')
        else:
            messages.error(request, _('Please correct the errors.'))
    else:
        user_form = SettingsForm(instance = current_user)
        password_form =  PasswordChangeForm(current_user)
        profile_form = ProfileForm(instance = current_user.profile)
        context = {"user": current_user, 'user_form': user_form, 'password_form': password_form, 'profile_form': profile_form}
        return render(request, 'account_settings.html', context=context)
