from django.urls import path
from . import views

app_name = 'indrel'
urlpatterns = [
    path('', views.index),
    path('resume-book', views.resume_book),
    path('resume-book/order', views.resume_book_order_form),
    path('infosessions', views.infosessions),
    path('infosession/registration', views.infosessions_registration),
    path('career-fair', views.career_fair),
    path('contact-us', views.contact_us, name="contact_us"),
]
