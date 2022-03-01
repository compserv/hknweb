from django.contrib import admin
from django.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .shortlinks import views as viewsShortlink
from hknweb.views import landing, users, indrel


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create/", users.account_create, name="account-create"),
    path("accounts/settings/", users.account_settings, name="account-settings"),
    path("accounts/activate/", users.activate),
    path("about/", landing.about, name="about"),
    path("academics/", include("hknweb.academics.urls")),
    path("events/", include("hknweb.events.urls")),
    path("alumni/", include("hknweb.alumni.urls")),
    path("studentservices/", include("hknweb.studentservices.urls")),
    path("serv/", include("hknweb.serv.urls")),
    path("tutoring/", include("hknweb.tutoring.urls")),
    path("cand/", include("hknweb.candidate.urls")),
    path("pages/", include("hknweb.markdown_pages.urls")),
    path("markdownx/", include("markdownx.urls")),
    path("course_surveys/", include("hknweb.course_surveys.urls")),
    path("auth/", include("social_django.urls", namespace="social")),
    path("", landing.home, name="home"),
    path("<slug:temp>/", viewsShortlink.openLink),
]

indrel_urlpatterns = [
    path("indrel", indrel.index, name="indrel"),
    path("indrel/resume_book", indrel.resume_book, name="resume_book"),
    path("indrel/infosessions", indrel.infosessions, name="infosessions"),
    path("indrel/career_fair", indrel.career_fair, name="career_fair"),
    path("indrel/contact_us", indrel.contact_us, name="contact_us"),
]

urlpatterns.extend(indrel_urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
