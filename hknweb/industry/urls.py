from django.urls import path

import hknweb.industry.views as views


app_name = "industry"
urlpatterns = [
    path("what_is_hkn", views.what_is_hkn, name="what_is_hkn"),
]