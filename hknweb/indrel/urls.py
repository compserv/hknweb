from django.urls import path
import hknweb.indrel.views as views

urlpatterns = [
    path("", views.indrel, name="indrel"),
    path("generate-resumebook/", views.generate_resumebook, name="generate_resumebook"),
]
