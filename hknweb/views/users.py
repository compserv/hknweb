import urllib
import json
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from hknweb.models import Profile
# import ast
from django.contrib.auth.models import User
from hknweb.forms import SettingsForm, ProfileForm, SignupForm, ValidPasswordForm, UpdatePasswordForm
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from hknweb.forms import SettingsForm, ProfileForm, SignupForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.conf import settings

def account_create(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if confirm_recaptcha(request):
                form.save()
            else:
                raise form.ValidationError('Invalid reCAPTCHA. Please try again.', code='invalid')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})

def confirm_recaptcha(request):
    if settings.DEBUG:
        return True
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result['success']
 
@login_required
def account_settings(request):
    current_user = request.user
    if request.method == 'POST':
        #user_form = SettingsForm(request.POST, instance = current_user)
        password_form = UpdatePasswordForm(current_user, request.POST)
        profile_form = ProfileForm(request.POST, instance = current_user.profile)
        verify_form = ValidPasswordForm(request.POST, instance = current_user.profile)
        #user_form.is_valid()
        #correct_password = authenticate(username=request.POST['username'], password=user_form.cleaned_data['password'])
        #if not correct_password:
        #    messages.error(request, ('Incorrect password. You must enter your password to save changes.'))
        #    return HttpResponseRedirect(request.path_info)
        #elif user_form.is_valid() and profile_form.is_valid() and password_form.is_valid():
        if verify_form.is_valid():
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, current_user)
                messages.success(request, ('Your password was successfully updated!'))
                return HttpResponseRedirect(request.path_info)
            if profile_form.is_valid():
                #user_form.save()
                profile_form.save()
                #user = password_form.save()
                update_session_auth_hash(request, current_user)
                messages.success(request, ('Your profile was successfully updated!'))
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, ('Please correct the errors.'))
                return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, ('Please enter current current password.'))
            return HttpResponseRedirect(request.path_info)
    else:
        # user_form = SettingsForm(instance = current_user)
        password_form = UpdatePasswordForm(current_user)
        profile_form = ProfileForm(instance = current_user.profile)
        verify_form = ValidPasswordForm(instance = current_user)
        #context = {"user": current_user, 'user_form': user_form, 'password_form': password_form, 'profile_form': profile_form}
        context = {'password_form': password_form, 'profile_form': profile_form, 'verify_form': verify_form}
        return render(request, 'account/settings.html', context=context)

@login_required
def activate(request):
    model = User
    field_names = ['username', 'email']
    data = [[getattr(ins, name) for name in field_names] for ins in model.objects.prefetch_related().all()]
    print(field_names)
    print(data)
    return render(request, 'account/activate.html', {'field_names': field_names, 'data': data})
