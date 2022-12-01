from django.http import HttpResponse

def index(request):
    return HttpResponse("Go to /polls or /admin")