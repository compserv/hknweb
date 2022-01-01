class Attr:
    COLOR = "color"
    COURSE = "course"
    COURSE_ID = "course_id"
    COURSE_SURVEYS_CSV = "course_surveys_csv"
    COURSES = "courses"
    DEPT = "dept"
    FORMAT = "format"
    ID = "id"
    INSTRUCTOR = "instructor"
    INSTRUCTOR_ID = "instructor_id"
    INSTRUCTOR_NAME = "instructor_name"
    INSTRUCTOR_TYPE = "instructor_type"
    INSTRUCTORS = "instructors"
    MAX = "max"
    NAME = "name"
    NEXT_PAGE = "next_page"
    NEXT_SURVEY = "next_survey"
    NUM_STUDENTS = "num_students"
    NUMBER = "number"
    PATH = "path"
    PAGE_NUMBER = "page_number"
    PAGES = "pages"
    PREVIOUS_PAGE = "previous_page"
    PREVIOUS_SURVEY = "previous_survey"
    RATINGS = "ratings"
    RESPONSE_COUNT = "response_count"
    SEARCH_BY = "search_by"
    SECTION_NUMBER = "section_number"
    SEMESTER = "semester"
    SERVICE = "service"
    STATUS = "status"
    SURVEY = "survey"
    SURVEY_NUMBER = "survey_number"
    TEXT = "text"
    TICKET = "ticket"
    TITLE = "title"
    UPLOAD_ALLOWED = "upload_allowed"
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
ITEMS_PER_PAGE = 10


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


class UploadStages:
    UPLOAD = "upload"
    QUESTIONS = "questions"
    INSTRUCTORS = "instructors"
    FINISHED = "finished"


class UploadStageInfo:
    UPLOAD = {
        Attr.TITLE: "Upload CSV",
        Attr.STATUS: UploadStages.UPLOAD,
    }
    QUESTIONS = {
        Attr.TITLE: "Merge questions",
        Attr.STATUS: UploadStages.QUESTIONS,
    }
    INSTRUCTORS = {
        Attr.TITLE: "Merge instructors",
        Attr.STATUS: UploadStages.INSTRUCTORS,
    }
    FINISHED = {
        Attr.TITLE: "Upload finished!",
        Attr.STATUS: UploadStages.FINISHED,
    }
