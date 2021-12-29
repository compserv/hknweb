import requests, json

from django.views.generic import TemplateView

from hknweb.markdown_pages.models import MarkdownPage
from hknweb.academics.models import Course, Instructor

from hknweb.course_surveys.constants import (
    Attr,
    CAS,
    COURSE_SURVEY_PREFIX,
    COURSE_SURVEY_TRANSPARENCY_PAGE_PATHS,
)


class IndexView(TemplateView):
    template_name = "course_surveys/index.html"

    def get_context_data(self, **kwargs):
        service = self.request.build_absolute_uri("?")
        cas_signed_in = self._validate_cas(service)

        context = {
            Attr.PAGES: self._get_pages(),
            Attr.SERVICE: service,
            Attr.COURSES: self._get_courses(cas_signed_in),
            Attr.INSTRUCTORS: self._get_instructors(cas_signed_in),
        }
        return context

    def _validate_cas(self, service: str) -> bool:
        """
        See https://apereo.github.io/cas/6.4.x/protocol/CAS-Protocol.html
        """
        ticket = self.request.GET.get(Attr.TICKET, None)
        if ticket is None:
            return False

        # See https://apereo.github.io/cas/6.4.x/protocol/CAS-Protocol-Specification.html
        params = {
            Attr.SERVICE: service,
            Attr.TICKET: ticket,
            Attr.FORMAT: CAS.JSON,
        }
        response = requests.get(CAS.SERVICE_VALIDATE_URL, params=params)
        content = json.loads(response.content.decode("utf-8"))
        response = content[CAS.SERVICE_RESPONSE]

        return CAS.AUTHENTICATION_SUCCESS in response

    @staticmethod
    def _get_courses(cas_signed_in: bool):
        if not cas_signed_in:
            return None

        courses = []
        seen_courses = set()
        for course in Course.objects.all():
            if not course.icsr_course.exists():
                continue

            most_recent_icsr = course.icsr_course.latest(
                "icsr_semester__year",
                "-icsr_semester__year_section",
            )

            key = "{dept} {number}".format(
                dept=most_recent_icsr.icsr_department.abbr,
                number=most_recent_icsr.course_number,
            )
            if key in seen_courses:
                continue

            seen_courses.add(key)
            courses.append(
                {
                    Attr.DEPT: most_recent_icsr.icsr_department.abbr,
                    Attr.NUMBER: most_recent_icsr.course_number,
                }
            )

        return courses

    @staticmethod
    def _get_instructors(cas_signed_in: bool):
        if not cas_signed_in:
            return None

        instructors = []
        seen_instructors = set()
        for instructor in Instructor.objects.all():
            if not instructor.icsr_instructor.exists():
                continue

            most_recent_icsr = instructor.icsr_instructor.latest(
                "icsr_semester__year",
                "-icsr_semester__year_section",
            )

            name = "{first_name} {last_name}".format(
                first_name=most_recent_icsr.first_name,
                last_name=most_recent_icsr.last_name,
            )

            key = name
            if key in seen_instructors:
                continue

            seen_instructors.add(key)
            instructors.append(
                {
                    Attr.NAME: name,
                }
            )

        return instructors

    @staticmethod
    def _get_pages():
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

        return pages
