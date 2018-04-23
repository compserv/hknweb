"""hknweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import login, logout
import hknweb.views as views

urlpatterns = [
    path('events/', include('hknweb.events.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include([
        path('profile/', views.account_settings),
        path('settings/', views.account_settings),
        path('login/', login, {'template_name': 'admin/login.html'}),
        path('logout/', logout),
    ]))
    
    url(r'^pages/', include('hknweb.markdown_pages.urls')),
    url(r'^markdownx/', include('markdownx.urls')),
]
