from django.shortcuts import render

from .models import Committee
from .models import Officer


def index(request):
    officers = Officer.objects.all()
    queryset = Committee.objects.all()
    committees = queryset.filter(is_exec=False)
    execs = queryset.filter(is_exec=True)

    context = {
        'committees': committees,
        'execs': execs,
        'officers': officers,
    }
    return render(request, 'officers/index.html', context)
