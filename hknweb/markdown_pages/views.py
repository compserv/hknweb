from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'markdown_pages/index.html', context)
