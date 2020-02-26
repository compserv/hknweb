from django.urls import path
from . import views

app_name = 'tours'
urlpatterns = [
    path('', views.tour, name='index'),
    # path('confirm', views.confirm, name='confirmtour'),
]
