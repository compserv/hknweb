import urllib
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from hknweb.forms import SettingsForm, ProfileForm, SignupForm, ValidPasswordForm, UpdatePasswordForm
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from hknweb.forms import SettingsForm, ProfileForm, SignupForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from hknweb.models import Profile, Semester
import datetime

# context processor for base to know whether a user is in the officer group
def add_officer_context(request):
    return {
        "viewer_is_an_officer":
            request.user.groups.filter(name=settings.OFFICER_GROUP).exists()
    }


# views

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
            
            profile = Profile.objects.get(user=user)
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
            profile.candidate_semester = Semester.objects.filter(semester=sem, year=str(now.year)).first()
            profile.save()

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
                if password_form.has_changed():
                    current_user = password_form.save()
                    update_session_auth_hash(request, current_user)
                    messages.success(request, ('Your password was successfully updated!'))
            else:
                messages.error(request, ('Please correct the errors in your Password: {}'.format(list(password_form.errors.values()))))

            if profile_form.is_valid():
                if profile_form.has_changed():
                    #user_form.save()
                    profile = profile_form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    #user = password_form.save()
                    update_session_auth_hash(request, current_user)
                    messages.success(request, ('Your profile was successfully updated!'))
            else:
                messages.error(request, ('Please correct the errors in your Profile data: {}'.format(list(profile_form.errors.values()))))
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
