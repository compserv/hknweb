from django.urls import path

import hknweb.serv.views as views


app_name = "serv"
urlpatterns = [
    path("", views.index, name="index"),
    path("eecsday", views.eecsday, name="eecsday"),
    path("jreecs", views.jreecs, name="jreecs"),
    path("bearhacks", views.bearhacks, name="bearhacks"),
    path("makershops", views.maker, name="makershops"),
    path("calday", views.calday, name="calday"),
]
