import requests, json

from django.views.generic import TemplateView

from hknweb.markdown_pages.models import MarkdownPage
from hknweb.academics.models import Course, Instructor

from hknweb.course_surveys.constants import (
    Attr,
    CAS,
    COLORS,
    COURSE_SURVEY_PREFIX,
    COURSE_SURVEY_TRANSPARENCY_PAGE_PATHS,
)


class IndexView(TemplateView):
    template_name = "course_surveys/index.html"

    def get_context_data(self, **kwargs):
        context = {}

        service = self.request.build_absolute_uri("?")
        cas_signed_in = self._validate_cas(service)

        survey_number = int(self.request.GET.get(Attr.SURVEY_NUMBER, 1))

        course, _context = self._get_course(
            cas_signed_in,
            self.request.GET.get(Attr.COURSE, None),
            survey_number,
        )
        context = {**context, **_context}

        instructor, _context = self._get_instructor(
            cas_signed_in,
            self.request.GET.get(Attr.INSTRUCTOR, None),
            survey_number,
        )
        context = {**context, **_context}

        context = {
            **context,
            Attr.PAGES: self._get_pages(),
            Attr.SERVICE: service,
            Attr.COURSES: self._get_courses(cas_signed_in),
            Attr.INSTRUCTORS: self._get_instructors(cas_signed_in),
            Attr.COURSE: course,
            Attr.INSTRUCTOR: instructor,
        }
        return context

    def _validate_cas(self, service: str) -> bool:
        """
        See https://apereo.github.io/cas/6.4.x/protocol/CAS-Protocol.html
        """
        cas_signed_in = self.request.session.get(CAS.SIGNED_IN, None)
        if cas_signed_in:
            return True

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
        print(content)
        response = content[CAS.SERVICE_RESPONSE]

        self.request.session[CAS.SIGNED_IN] = CAS.AUTHENTICATION_SUCCESS in response

        return self.request.session[CAS.SIGNED_IN]

    @staticmethod
    def _get_courses(cas_signed_in: bool):
        if not cas_signed_in:
            return None

        courses = []
        seen_courses = set()
        for course in Course.objects.all():
            if not course.icsr_course.exists():
                continue

            icsrs = course.icsr_course.filter(
                section_number__exact="1", instructor_type__exact="Professor"
            )
            if not icsrs.exists():
                continue

            most_recent_icsr = icsrs.latest(
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
                    Attr.NAME: most_recent_icsr.course_name,
                    Attr.ID: course.id,
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
                    Attr.ID: instructor.instructor_id,
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

    @staticmethod
    def _get_course(cas_signed_in, id, survey_number):
        if not cas_signed_in or id is None:
            return None, {}

        course = Course.objects.get(pk=id)

        icsrs = course.icsr_course.order_by(
            "-icsr_semester__year",
            "icsr_semester__year_section",
        ).filter(section_number__exact="1", instructor_type__exact="Professor")
        most_recent_icsr = icsrs.first()

        if survey_number > len(icsrs):
            return None, {}
        icsr = icsrs[survey_number - 1]

        course_context = {
            Attr.DEPT: most_recent_icsr.icsr_department.abbr,
            Attr.NUMBER: most_recent_icsr.course_number,
            Attr.NAME: most_recent_icsr.course_name,
            Attr.ID: course.id,
        }
        context = {
            Attr.SURVEY: IndexView._get_survey(icsr),
            Attr.PREVIOUS_PAGE: survey_number - 1 if survey_number > 1 else None,
            Attr.NEXT_PAGE: survey_number + 1 if survey_number < len(icsrs) else None,
        }
        return course_context, context

    @staticmethod
    def _get_instructor(cas_signed_in, id, survey_number):
        if not cas_signed_in or id is None:
            return None, {}

        instructor = Instructor.objects.get(pk=id)

        icsrs = instructor.icsr_instructor.order_by(
            "-icsr_semester__year",
            "icsr_semester__year_section",
        )
        most_recent_icsr = icsrs.first()

        if survey_number > len(icsrs):
            return None, {}
        icsr = icsrs[survey_number - 1]

        name = "{first_name} {last_name}".format(
            first_name=most_recent_icsr.first_name,
            last_name=most_recent_icsr.last_name,
        )

        instructor_context = {
            Attr.NAME: name,
            Attr.ID: instructor.instructor_id,
            Attr.INSTRUCTOR_TYPE: most_recent_icsr.instructor_type,
        }
        context = {
            Attr.SURVEY: IndexView._get_survey(icsr),
            Attr.PREVIOUS_PAGE: survey_number - 1 if survey_number > 1 else None,
            Attr.NEXT_PAGE: survey_number + 1 if survey_number < len(icsrs) else None,
        }
        return instructor_context, context

    @staticmethod
    def _get_survey(icsr):
        semester = icsr.icsr_semester
        survey = icsr.survey_icsr.first()

        ratings = []
        for rating in survey.rating_survey.all():
            percent = rating.rating_value / rating.range_max
            color = COLORS.FIRE_BRICK
            if rating.inverted:
                if percent < 0.2:
                    color = COLORS.FOREST_GREEN
                elif percent < 0.4:
                    color = COLORS.GOLDEN_ROD
            else:
                if percent > 0.8:
                    color = COLORS.FOREST_GREEN
                elif percent > 0.6:
                    color = COLORS.GOLDEN_ROD

            ratings.append(
                {
                    Attr.TEXT: rating.question_text,
                    Attr.MAX: rating.range_max,
                    Attr.VALUE: rating.rating_value,
                    Attr.COLOR: color,
                }
            )

        return {
            Attr.DEPT: icsr.icsr_department.abbr,
            Attr.NUMBER: icsr.course_number,
            Attr.COURSE_ID: icsr.icsr_course.id,
            Attr.SECTION_NUMBER: icsr.section_number,
            Attr.SEMESTER: semester.year_section + str(semester.year)[-2:],
            Attr.INSTRUCTOR_TYPE: icsr.instructor_type,
            Attr.NUM_STUDENTS: survey.num_students,
            Attr.RESPONSE_COUNT: survey.response_count,
            Attr.RATINGS: ratings,
        }
