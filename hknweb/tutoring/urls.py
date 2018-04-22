from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^future/$', views.future, name='future'),
	url(r'^past/$', views.past, name='past'),
	url(r'^$', views.index)
]