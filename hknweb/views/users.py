from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from hknweb.models import Profile
# import ast
from django.contrib.auth.models import User
from hknweb.forms import SettingsForm, ProfileForm, SignupForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages

def account_create(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
             form.save()
             username = form.cleaned_data.get('username')
             raw_password = form.cleaned_data.get('password1')
             user = authenticate(username = username, password = raw_password)
             login(request, user)
             return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required
def account_settings(request):
    current_user = request.user
    if request.method == 'POST':
        #user_form = SettingsForm(request.POST, instance = current_user)
        #password_form = PasswordChangeForm(current_user, request.POST)
        profile_form = ProfileForm(request.POST, instance = current_user.profile)
        #user_form.is_valid()
        #correct_password = authenticate(username=request.POST['username'], password=user_form.cleaned_data['password'])
        #if not correct_password:
        #    messages.error(request, ('Incorrect password. You must enter your password to save changes.'))
        #    return HttpResponseRedirect(request.path_info)
        #elif user_form.is_valid() and profile_form.is_valid() and password_form.is_valid():
        if profile_form.is_valid():
            #user_form.save()
            profile_form.save()
            #user = password_form.save()
            #update_session_auth_hash(request, user)
            messages.success(request, ('Your profile was successfully updated!'))
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, ('Please correct the errors.'))
            return HttpResponseRedirect(request.path_info)
    else:
        #user_form = SettingsForm(instance = current_user)
        #password_form =  PasswordChangeForm(current_user)
        profile_form = ProfileForm(instance = current_user.profile)
        #context = {"user": current_user, 'user_form': user_form, 'password_form': password_form, 'profile_form': profile_form}
        context = {'profile_form': profile_form}
        return render(request, 'account/settings.html', context=context)
