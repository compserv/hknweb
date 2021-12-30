class Attr:
    COLOR = "color"
    COURSE = "course"
    COURSE_ID = "course_id"
    COURSES = "courses"
    DEPT = "dept"
    FORMAT = "format"
    ID = "id"
    INSTRUCTOR = "instructor"
    INSTRUCTOR_TYPE = "instructor_type"
    INSTRUCTORS = "instructors"
    MAX = "max"
    NAME = "name"
    NEXT_PAGE = "next_page"
    NUM_STUDENTS = "num_students"
    NUMBER = "number"
    PATH = "path"
    PAGES = "pages"
    PREVIOUS_PAGE = "previous_page"
    RATINGS = "ratings"
    RESPONSE_COUNT = "response_count"
    SECTION_NUMBER = "section_number"
    SEMESTER = "semester"
    SERVICE = "service"
    SURVEY = "survey"
    SURVEY_NUMBER = "survey_number"
    TEXT = "text"
    TICKET = "ticket"
    VALUE = "value"


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


class COLORS:
    FIRE_BRICK = "FireBrick"
    FOREST_GREEN = "ForestGreen"
    GOLDEN_ROD = "GoldenRod"
