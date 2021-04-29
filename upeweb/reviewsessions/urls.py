from django.urls import path
from . import views

app_name = 'reviewsessions'
urlpatterns = [
    path(r'<int:id>', views.show_details, name='detail'),
    path('new', views.add_reviewsession),
    path(r'<int:pk>/edit', views.ReviewSessionUpdateView.as_view(), name='edit'),
    path(r'', views.index, name='index'),
]
