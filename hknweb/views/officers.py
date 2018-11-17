from django.shortcuts import render

from hknweb.models import Committee
from hknweb.models import Officer


def index(request):
    officers = Officer.objects.all()
    all_committees = Committee.objects.all()
    committees = all_committees.filter(is_exec=False)
    execs = all_committees.filter(is_exec=True)

    context = {
        'committees': committees,
        'execs': execs,
        'officers': officers,
    }
    return render(request, 'officers/index.html', context)
