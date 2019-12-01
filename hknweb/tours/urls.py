from django.urls import path
from . import views

app_name = 'tours'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('confirm', views.ConfirmView.as_view(), name='confirmtour'),
]
