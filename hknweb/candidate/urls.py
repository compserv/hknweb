from django.urls import path

from . import views

app_name = 'candidate'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # candidate end of officer challenge requests
    path('candreq', views.CandRequestView.as_view(), name='candrequests'),
    # officer end of officer challenge requests
    # currently dummy page, goes to index
    path('offreq', views.IndexView.as_view(), name='offrequests'),
]
