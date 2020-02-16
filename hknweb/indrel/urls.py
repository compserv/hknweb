from django.urls import path
from . import views

app_name = 'indrel'
urlpatterns = [
    path('', views.index),
    path('resume-book', views.resume_book, name="resume_book"),
    path('resume-book/order', views.ResumeBookOrderFormView.as_view(), name="resume_book/order"),
    path('infosessions', views.infosessions, name="infosessions"),
    path('infosessions/registration', views.InfosessionRegistrationView.as_view(), name="infosessions/registration"),
    path('career-fair', views.career_fair),
    path('contact-us', views.contact_us, name="contact_us"),
]
