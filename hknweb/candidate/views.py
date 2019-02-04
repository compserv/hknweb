from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'candidate/index.html'

class CandRequestView(generic.TemplateView):
    template_name = 'candidate/candreq.html'
