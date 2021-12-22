from django.urls import path
from . import views

app_name = 'indrel'
urlpatterns = [
    path('', views.index, name="index"),
    path('resume-book', views.resume_book, name="resume_book"),
    path('infosessions', views.infosessions, name="infosessions"),
    path('career-fair', views.career_fair, name="career_fair"),
    path('contact-us', views.contact_us, name="contact_us"),
]
