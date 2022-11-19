import markdownx.views as markdownx_views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .shortlinks import views as viewsShortlink
from hknweb.views import landing, users, indrel, serv, people
from .utils import method_login_and_permission

__all__ = ["urlpatterns", "safe_urlpatterns"]

# DO NOT add urls here unless you know what you are doing
unsafe_urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("auth/", include("social_django.urls", namespace="social")),
]

app_urlpatterns = [
    path("accounts/create/", users.account_create, name="account-create"),
    path("accounts/settings/", users.account_settings, name="account-settings"),
    path("about/", landing.about, name="about"),
    path("academics/", include("hknweb.academics.urls")),
    path("events/", include("hknweb.events.urls")),
    path("alumni/", include("hknweb.alumni.urls")),
    path("studentservices/", include("hknweb.studentservices.urls")),
    path("tutoring/", include("hknweb.tutoring.urls")),
    path("cand/", include("hknweb.candidate.urls")),
    path("polls/", include("hknweb.polls.urls")),
    path("pages/", include("hknweb.markdown_pages.urls")),
    path("course_surveys/", include("hknweb.course_surveys.urls")),
    path("", landing.home, name="home"),
    path("<slug:temp>/", viewsShortlink.openLink),
    path("about/people/", people.people, name="people"),
]

markdownx_urlpatterns = [
    url(
        r"^markdownx/upload/$",
        method_login_and_permission("markdown_pages.add_markdownpage")(
            markdownx_views.ImageUploadView
        ).as_view(),
        name="markdownx_upload",
    ),
    url(
        r"^markdownx/markdownify/$",
        method_login_and_permission("markdown_pages.add_markdownpage")(
            markdownx_views.MarkdownifyView
        ).as_view(),
        name="markdownx_markdownify",
    ),
]

indrel_urlpatterns = [
    path("indrel", indrel.index, name="indrel"),
    path("indrel/resume_book", indrel.resume_book, name="resume_book"),
    path("indrel/infosessions", indrel.infosessions, name="infosessions"),
    path("indrel/career_fair", indrel.career_fair, name="career_fair"),
    path("indrel/contact_us", indrel.contact_us, name="contact_us"),
]

serv_urlpatterns = [
    path("serv", serv.index, name="serv"),
    path("serv/eecsday", serv.eecsday, name="eecsday"),
    path("serv/jreecs", serv.jreecs, name="jreecs"),
    path("serv/bearhacks", serv.bearhacks, name="bearhacks"),
    path("serv/makershops", serv.maker, name="makershops"),
    path("serv/calday", serv.calday, name="calday"),
]

safe_urlpatterns = [
    *app_urlpatterns,
    *markdownx_urlpatterns,
    *indrel_urlpatterns,
    *serv_urlpatterns,
]

urlpatterns = [
    *unsafe_urlpatterns,
    *safe_urlpatterns,
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
