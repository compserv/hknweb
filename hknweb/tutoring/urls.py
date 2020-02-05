from django.urls import path

from . import views

app_name = 'tutoring'
urlpatterns = [
    path(r'', views.index, name='index'),
    path('new', views.tutor_class_preference),
    path(r'generate', views.generate_schedule),
]
