from django.shortcuts import render

def index(request):
    return render(request, 'indrel/index.html')

def resume_book(request):
    return render(request, 'indrel/resume_book.html')

def infosessions(request):
    return render(request, 'indrel/infosessions.html')

def career_fair(request):
    return render(request, 'indrel/career_fair.html')

def contact_us(request):
    return render(request, 'indrel/contact_us.html')

def resume_book_order_form(request):
    return render(request, 'indrel/resume_book_order_form.html')

def infosessions_registration(request):
    return render(request, 'indrel/infosessions_registration.html')

def order_resume_book(request):
    pass

def register_info_session(request):
    pass