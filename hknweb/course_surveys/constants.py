class Attr:
    COURSES = "courses"
    DEPT = "dept"
    FORMAT = "format"
    INSTRUCTORS = "instructors"
    NAME = "name"
    NUMBER = "number"
    PATH = "path"
    PAGES = "pages"
    SERVICE = "service"
    TICKET = "ticket"


COURSE_SURVEY_TRANSPARENCY_PAGE_PATHS = [
    "course_surveys_authentication",
    "course_surveys_infrastructure",
    "course_surveys_upload",
    "course_surveys_visualization",
    "course_surveys_database",
    "course_surveys_management",
    "course_surveys_permissions",
    "course_surveys_search",
]

COURSE_SURVEY_PREFIX = "Course surveys "


class CAS:
    AUTHENTICATION_SUCCESS = "authenticationSuccess"
    JSON = "JSON"
    SIGNED_IN = "signed_in"
    SERVICE_RESPONSE = "serviceResponse"
    SERVICE_VALIDATE_URL = "https://auth.berkeley.edu/cas/serviceValidate"
