from django.shortcuts import render
from .forms import DocumentForm

def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            print(form)
            print("form was valid")
            form.save()
            return render(request, 'resume/uploaded.html')  
        else:
            print("Form wasnt valid")
            form = DocumentForm()
            return render(request, 'resume/index.html', {
                'form': form,
                'err': True,
            })

    form = DocumentForm()
    return render(request, 'resume/index.html', {
        'form': form,
        'err': False,
    })


def submitted(request):
    form = DocumentForm()
    return render(request, 'resume/index.html', {
        'form': form
    })
    
