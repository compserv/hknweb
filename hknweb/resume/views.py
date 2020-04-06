from django.shortcuts import render
from .forms import DocumentForm

# Create your views here.
# def model_form_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = DocumentForm()
#     return render(request, 'core/model_form_upload.html', {
#         'form': form
#     })

def index(request):
    form = DocumentForm()
    return render(request, 'resume/index.html', {
        'form': form
    })


def submitted(request):
    form = DocumentForm()
    return render(request, 'resume/index.html', {
        'form': form
    })
    
