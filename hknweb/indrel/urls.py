from django.urls import path
from . import views

app_name = 'indrel'
urlpatterns = [
    path('', views.index),
    path('resume-book', views.resume_book),
    path('infosessions', views.infosessions),
    path('career-fair', views.career_fair),
    path('contact-us', views.contact_us, name="contact_us"),
]
