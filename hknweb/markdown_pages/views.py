from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from markdownx.utils import markdownify

from .models import MarkdownPage
from .forms import EditPageForm

def editor(request):
    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            mdp = MarkdownPage(**form.cleaned_data)
            mdp.save()
            return redirect(display, path=mdp.path)
    else:
        form = EditPageForm()

    return render(request, 'markdown_pages/editor.html', { 'form': form })

def display(request, path):
    mdp = get_object_or_404(MarkdownPage, path=path)
    return render(request, 'markdown_pages/display.html', {
        'name': mdp.name,
        'body': markdownify(mdp.body),
    })
