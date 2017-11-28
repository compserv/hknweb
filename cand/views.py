# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
	return redirect('portal')

def portal(request):
	template = loader.get_template('portal.html')
	context = {}
	return HttpResponse(template.render(context, request))