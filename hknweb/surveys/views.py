from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'surveys/index.html', context)
