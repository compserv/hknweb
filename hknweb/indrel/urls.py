from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'indrel'
urlpatterns = [
    path('', views.index),
    path('resume-book', views.resume_book, name="resume_book"),
    path('resume-book/order', views.ResumeBookOrderFormView.as_view(), name="resume_book/order"),
    path('infosessions', views.infosessions, name="infosessions"),
    path('infosessions/registration', views.InfosessionRegistrationView.as_view(), name="infosessions/registration"),
    path('career-fair', views.career_fair),
    path('contact-us', views.contact_us, name="contact_us"),
    path('mailer',views.mailer,name="mailer"),
    # path('mailer',views.mailer,name="mailer"),
    path('thanks',TemplateView.as_view(template_name="indrel/thanks.html"),name='thanks')

]
