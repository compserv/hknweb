from django.urls import path

from . import views

app_name = 'tutoring'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'generate', views.generate_schedule, name='generate'),
    path(r'slotpref', views.tutor_slot_preference, name='slotpref'),
    path(r'coursepref', views.tutor_course_preference, name='coursepref')
]
