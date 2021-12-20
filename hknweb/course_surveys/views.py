from django.shortcuts import render

from hknweb.markdown_pages.models import MarkdownPage

from hknweb.course_surveys.constants import (
    Attr,
    COURSE_SURVEY_PREFIX,
    COURSE_SURVEY_TRANSPARENCY_PAGE_PATHS,
)


def index(request):
    pages = []
    for page_path in COURSE_SURVEY_TRANSPARENCY_PAGE_PATHS:
        page = MarkdownPage.objects.filter(path=page_path).first()
        if page is not None:
            page_name = page.name
            if page_name.startswith(COURSE_SURVEY_PREFIX):
                page_name = page_name[len(COURSE_SURVEY_PREFIX) :]

            pages.append(
                {
                    Attr.NAME: page_name,
                    Attr.PATH: "/pages/" + page_path,
                }
            )

    context = {
        Attr.PAGES: pages,
    }

    return render(request, "course_surveys/index.html", context)
