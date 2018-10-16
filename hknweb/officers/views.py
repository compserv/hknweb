from django.shortcuts import render

from .models import Committee
from .models import Officer


def index(request):
    officers = Officer.objects.all()
    committees = Committee.objects.all()

    context = {
        'committees': committees,
        'officers': officers,
    }
    return render(request, 'officers/index.html', context)
