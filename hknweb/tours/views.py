from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'tours/index.html', context)
