from django.urls import path

from . import views

app_name = 'dept_tours'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('request/<int:pk>/', views.request_submitted, name="request")
]