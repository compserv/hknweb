from django.urls import path, re_path

from . import views

app_name = 'candidate'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # candidate end of officer challenge requests
    path('candreq', views.CandRequestView.as_view(), name='candrequests'),
    # officer end of officer challenge requests
    re_path(r'^challengeconfirm/(?P<pk>\d+)/$', views.officer_confirm_view, name='challengeconfirm'),
    re_path(r'^detail/(?P<pk>\d+)/$', views.challenge_detail_view, name='detail'),
    re_path(r'^reviewconfirm/(?P<pk>\d+)/$', views.officer_review_confirmation, name='reviewconfirm'),
    # dummy url for now
    path('dummy', views.IndexView.as_view(), name='dummy'),
]
