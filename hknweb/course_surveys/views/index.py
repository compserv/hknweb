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
    ITEMS_PER_PAGE,
)


class IndexView(TemplateView):
    template_name = "course_surveys/index.html"

    def get_context_data(self, **kwargs):
        context = {}

        # Setup various attribute variables
        service = self.request.build_absolute_uri("?")
        upload_allowed = self.request.user.has_perm(
            "course_surveys.change_academicentity"
        )
        cas_signed_in = self._validate_cas(service)

        # Get pagination information
        page_number = int(self.request.GET.get(Attr.PAGE_NUMBER, 1))
        survey_number = int(self.request.GET.get(Attr.SURVEY_NUMBER, 1))

        # Retrieve courses and instructors for search panel
        search_by = self.request.GET.get(Attr.SEARCH_BY, Attr.COURSES)
        courses, _context = self._get_courses(cas_signed_in, search_by, page_number)
        context = {**context, **_context}
        instructors, _context = self._get_instructors(
            cas_signed_in, search_by, page_number
        )
        context = {**context, **_context}

        # Retrieve specific course or instructor based on query params
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

        # Create context and return
        return {
            **context,
            Attr.PAGES: self._get_pages(),
            Attr.UPLOAD_ALLOWED: upload_allowed,
            Attr.SERVICE: service,
            Attr.COURSES: courses,
            Attr.INSTRUCTORS: instructors,
            Attr.COURSE: course,
            Attr.INSTRUCTOR: instructor,
        }

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
        response = content[CAS.SERVICE_RESPONSE]

        self.request.session[CAS.SIGNED_IN] = CAS.AUTHENTICATION_SUCCESS in response

        return self.request.session[CAS.SIGNED_IN]

    @staticmethod
    def _get_courses(cas_signed_in: bool, search_by: str, page_number: int):
        if not cas_signed_in or search_by != Attr.COURSES:
            return None, {}

        courses = []
        i_start, i_end = IndexView._get_start_end_indices(page_number)
        for course in Course.objects.all()[i_start:i_end]:
            icsrs = course.icsr_course.filter(
                section_number__exact="1", instructor_type__exact="Professor"
            )
            if not icsrs.exists():
                icsrs = course.icsr_course.all()

            most_recent_icsr = icsrs.latest(
                "icsr_semester__year",
                "-icsr_semester__year_section",
            )

            courses.append(
                {
                    Attr.DEPT: most_recent_icsr.icsr_department.abbr,
                    Attr.NUMBER: most_recent_icsr.course_number,
                    Attr.NAME: most_recent_icsr.course_name,
                    Attr.ID: course.id,
                }
            )

        return courses, IndexView._get_pagination_info(
            page_number, Course.objects.count()
        )

    @staticmethod
    def _get_instructors(cas_signed_in: bool, search_by: str, page_number: int):
        if not cas_signed_in or search_by != Attr.INSTRUCTORS:
            return None, {}

        instructors = []
        i_start, i_end = IndexView._get_start_end_indices(page_number)
        for instructor in Instructor.objects.all()[i_start:i_end]:
            most_recent_icsr = instructor.icsr_instructor.latest(
                "icsr_semester__year",
                "-icsr_semester__year_section",
            )

            name = "{first_name} {last_name}".format(
                first_name=most_recent_icsr.first_name,
                last_name=most_recent_icsr.last_name,
            )

            instructors.append(
                {
                    Attr.NAME: name,
                    Attr.ID: instructor.instructor_id,
                }
            )

        return instructors, IndexView._get_pagination_info(
            page_number, Instructor.objects.count()
        )

    @staticmethod
    def _get_start_end_indices(page_number: int):
        i_start = ITEMS_PER_PAGE * (page_number - 1)
        i_end = ITEMS_PER_PAGE * page_number

        return i_start, i_end

    @staticmethod
    def _get_pagination_info(page_number: int, n: int):
        return {
            Attr.PREVIOUS_PAGE: page_number - 1 if page_number > 1 else None,
            Attr.NEXT_PAGE: page_number + 1
            if (page_number * ITEMS_PER_PAGE) < n
            else None,
        }

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
        )
        icsrs_filtered = icsrs.filter(
            section_number__exact="1", instructor_type__exact="Professor"
        )
        if icsrs_filtered.exists():
            icsrs = icsrs_filtered

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
        return course_context, IndexView._get_survey_context(
            icsr, len(icsrs), survey_number
        )

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
        return instructor_context, IndexView._get_survey_context(
            icsr, len(icsrs), survey_number
        )

    @staticmethod
    def _get_survey_context(icsr, n_icsrs, survey_number):
        return {
            Attr.SURVEY: IndexView._get_survey(icsr),
            Attr.PREVIOUS_SURVEY: survey_number - 1 if survey_number > 1 else None,
            Attr.NEXT_SURVEY: survey_number + 1 if survey_number < n_icsrs else None,
        }

    @staticmethod
    def _get_survey(icsr):
        semester = icsr.icsr_semester
        instructor = icsr.icsr_instructor

        context = {
            Attr.DEPT: icsr.icsr_department.abbr,
            Attr.NUMBER: icsr.course_number,
            Attr.COURSE_ID: icsr.icsr_course.id,
            Attr.INSTRUCTOR_ID: instructor.instructor_id,
            Attr.INSTRUCTOR_NAME: "%s %s" % (icsr.first_name, icsr.last_name),
            Attr.SECTION_NUMBER: icsr.section_number,
            Attr.SEMESTER: semester.year_section + str(semester.year)[-2:],
            Attr.INSTRUCTOR_TYPE: icsr.instructor_type,
            Attr.RATINGS: None,
        }
        if not icsr.survey_icsr.exists():
            return context
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
                    Attr.VALUE: round(rating.rating_value, 2),
                    Attr.COLOR: color,
                }
            )

        return {
            **context,
            Attr.NUM_STUDENTS: survey.num_students,
            Attr.RESPONSE_COUNT: survey.response_count,
            Attr.RATINGS: ratings,
        }
