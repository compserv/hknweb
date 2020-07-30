from .course_surveys_views import (
    QuestionViewSet,
    RatingViewSet,
    SurveyViewSet,
)

from .icsr_views import ICSRViewSet

from .logistics_views import (
    CourseViewSet,
    DepartmentViewSet,
    InstructorViewSet,
    SemesterViewSet,
)


def register_viewsets(router):
    router.register(r'questions', QuestionViewSet)
    router.register(r'ratings', RatingViewSet)
    router.register(r'surveys', SurveyViewSet)
    router.register(r'icsrs', ICSRViewSet)
    router.register(r'courses', CourseViewSet)
    router.register(r'departments', DepartmentViewSet)
    router.register(r'instructors', InstructorViewSet)
    router.register(r'semesters', SemesterViewSet)
