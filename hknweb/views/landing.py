from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse
from hknweb.models import Profile
# import ast
from django.contrib.auth.models import User
from hknweb.forms import SettingsForm, ProfileForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render


def home(request):
    return render(request, 'landing/home.html')