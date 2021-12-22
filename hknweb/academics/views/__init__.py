from hknweb.academics.views.course_surveys import (
    QuestionViewSet,
    RatingViewSet,
    SurveyViewSet,
)
from hknweb.academics.views.logistics import (
    CourseViewSet,
    DepartmentViewSet,
    InstructorViewSet,
    SemesterViewSet,
)
from hknweb.academics.views.icsr import ICSRViewSet


def register_viewsets(router):
    router.register(r"questions", QuestionViewSet)
    router.register(r"ratings", RatingViewSet)
    router.register(r"surveys", SurveyViewSet)
    router.register(r"icsrs", ICSRViewSet)
    router.register(r"courses", CourseViewSet)
    router.register(r"departments", DepartmentViewSet)
    router.register(r"instructors", InstructorViewSet)
    router.register(r"semesters", SemesterViewSet)
