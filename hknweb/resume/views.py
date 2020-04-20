from django.shortcuts import render
from .forms import DocumentForm
from django.core.files.storage import FileSystemStorage

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
 #  if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = DocumentForm()
#     return render(request, 'core/model_form_upload.html', {
#         'form': form
#     })
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
        #     fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        # return render(request, 'resume/uploaded.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })

    form = DocumentForm()
    return render(request, 'resume/index.html', {
        'form': form
    })


def submitted(request):
    form = DocumentForm()
    return render(request, 'resume/index.html', {
        'form': form
    })
    
