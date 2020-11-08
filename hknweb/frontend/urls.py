from django.urls import path
from . import views


urlpatterns = [
    path('academics/departments', views.DepartmentsView.as_view()),
    path('academics/instructors', views.InstructorsView.as_view()),
]
