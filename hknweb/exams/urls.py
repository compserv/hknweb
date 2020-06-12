from django.conf.urls import url
from django.urls import path, re_path
# from .exam_autocomplete import CourseSemesterAutocomplete

from . import views

urlpatterns = [
	path('course/<department>/<number>/', views.exams_for_course),
    path('new/', views.add_exam),
    path('', views.index),
    # re_path(
    #     r'^courseSemester-autocomplete/$',
    #     CourseSemesterAutocomplete.as_view(),
    #     name='courseSemester-autocomplete',
    # )
]
