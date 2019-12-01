from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'guide/index.html', context)
