from django.urls import path, re_path

from . import views

app_name = 'candidate'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # candidate end of officer challenge requests
    path('candreq', views.CandRequestView.as_view(), name='candrequests'),
    # officer end of officer challenge requests
    path('offreq', views.OffRequestView.as_view(), name='offrequests'),
    path('challengeconfirm/<int:pk>/', views.officer_confirm_view, name='challengeconfirm'),
    path('detail/<int:pk>/', views.challenge_detail_view, name='detail'),
    path('reviewconfirm/<int:pk>/', views.officer_review_confirmation, name='reviewconfirm'),
]
