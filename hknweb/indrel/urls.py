from django.urls import path
import hknweb.indrel.views as views

urlpatterns = [
    path("", views.indrel, name="indrel"),
    path("generate-resumebook/", views.generate_resumebook, name="generate_resumebook"),
    path("portal", views.indrelportal, name="indrel_portal"),
    path("portal", views.indrelportal, name="indrel_events"),
    path("portal", views.indrelportal, name="indrel_locations"),
    path("portal", views.indrelportal, name="indrel_companies"),
    path("portal", views.indrelportal, name="indrel_contacts"),
    path("portal", views.indrelportal, name="indrel_types"),
    path("resumebooks", views.resumebooks, name="indrel_resumebooks"),
]
