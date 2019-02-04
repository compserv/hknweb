from django.urls import path

from . import views

app_name = 'alumni'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # candidate end of officer challenge requests
    path('candrequests', views.IndexView.as_view(), name='candrequests'),
    # officer end of officer challenge requests
    path('offrequests', views.IndexView.as_view(), name='offrequests'),
]
