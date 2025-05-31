import markdownx.views as markdownx_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from hknweb.utils import method_login_and_permission
from hknweb.views import indrel, landing, outreach, people, users, bitbyte_tree

__all__ = ["urlpatterns", "safe_urlpatterns"]

# DO NOT add urls here unless you know what you are doing
unsafe_urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

app_urlpatterns = [
    path("accounts/create/", users.account_create, name="account-create"),
    path("accounts/settings/", users.account_settings, name="account-settings"),
    path("academics/", include("hknweb.academics.urls")),
    path("events/", include("hknweb.events.urls")),
    path("studentservices/", include("hknweb.studentservices.urls")),
    path("tutoring/", include("hknweb.tutoring.urls")),
    path("cand/", include("hknweb.candidate.urls")),
    path("pages/", include("hknweb.markdown_pages.urls")),
    path("course_surveys/", include("hknweb.course_surveys.urls")),
    path("", landing.home, name="home"),
    # TODO: refactor about to be its own module.
    path("about/", landing.about, name="about"),
    path("about/people/", people.people, name="people"),
    path("about/bitbyte_tree_data", bitbyte_tree.bitbyte_tree_data, name="bitbyte_tree_data"),
    path("about/bitbyte_tree", bitbyte_tree.bitbyte_tree, name="bitbyte_tree"),
    path("indrel", indrel.indrel, name="indrel"),
    path("outreach", outreach.outreach, name="outreach"),
]

markdownx_urlpatterns = [
    path(
        "markdownx/upload/",
        method_login_and_permission("markdown_pages.add_markdownpage")(
            markdownx_views.ImageUploadView
        ).as_view(),
        name="markdownx_upload",
    ),
    path(
        "markdownx/markdownify/",
        method_login_and_permission("markdown_pages.add_markdownpage")(
            markdownx_views.MarkdownifyView
        ).as_view(),
        name="markdownx_markdownify",
    ),
]

safe_urlpatterns = [
    *app_urlpatterns,
    *markdownx_urlpatterns,
]

urlpatterns = [
    *unsafe_urlpatterns,
    *safe_urlpatterns,
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
