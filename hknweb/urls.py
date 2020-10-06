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
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import landing
from .views import users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create/', users.account_create, name='account-create'),
    path('accounts/settings/', users.account_settings, name='account-settings'),
    path('accounts/activate/', users.activate),
    path('about/', landing.about, name='about'),
    path('events/', include('hknweb.events.urls')),
    path('reviewsessions/', include('hknweb.reviewsessions.urls')),
    path('exams/', include('hknweb.exams.urls')),
    path('alumni/', include('hknweb.alumni.urls')),
    path('tutoring/', include('hknweb.tutoring.urls')),
    path('tours/', include('hknweb.tours.urls')),
    path('cand/', include('hknweb.candidate.urls')),
    path('pages/', include('hknweb.markdown_pages.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('s/', include('hknweb.shortlinks.urls')),
    path('elections/', include('hknweb.elections.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('', landing.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
