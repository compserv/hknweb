class Attr:
    BACK = "back"
    COLOR = "color"
    COURSE = "course"
    COURSE_ID = "course_id"
    COURSE_SURVEYS_CSV = "course_surveys_csv"
    COURSES = "courses"
    DEPT = "dept"
    EXISTING_INSTRUCTORS = "existing_instructors"
    EXISTING_QUESTIONS = "existing_questions"
    FORMAT = "format"
    ID = "id"
    INSTRUCTOR = "instructor"
    INSTRUCTOR_ID = "instructor_id"
    INSTRUCTOR_IDS = "instructor_ids"
    INSTRUCTOR_NAME = "instructor_name"
    INSTRUCTOR_TYPE = "instructor_type"
    INSTRUCTORS = "instructors"
    MAX = "max"
    NAME = "name"
    NEXT = "next"
    NEXT_PAGE = "next_page"
    NEXT_STATUS = "next_status"
    NEXT_SURVEY = "next_survey"
    NUM_STUDENTS = "num_students"
    NUMBER = "number"
    QUESTION_IDS = "question_ids"
    PATH = "path"
    PAGE_NUMBER = "page_number"
    PAGES = "pages"
    PREVIOUS_PAGE = "previous_page"
    PREVIOUS_STATUS = "previous_status"
    PREVIOUS_SURVEY = "previous_survey"
    RATINGS = "ratings"
    RESPONSE_COUNT = "response_count"
    SEARCH_BY = "search_by"
    SEARCH_VALUE = "search_value"
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
COURSE_SURVEYS_EDIT_PERMISSION = "academics.change_academicentity"


class CAS:
    AUTHENTICATION_SUCCESS = "authenticationSuccess"
    JSON = "JSON"
    SIGNED_IN = "signed_in"
    SERVICE_RESPONSE = "serviceResponse"
    SERVICE_VALIDATE_URL = "https://auth.berkeley.edu/cas/serviceValidate"


# HSL tuples for interpolation for rating colors
# e.g. 7/7 maps to green = hsl(120, 61%, 34%)
# the red hue must be less than the yellow hue so that the color 
# interpolated between red and yellow is orange instead of blue,
# so just use 0 instead of 360. negative hues work fine.
class COLORS:
    RED = (0, 68, 42)
    YELLOW = (43, 75, 49)
    GREEN = (120, 61, 34)
    # the score at which the exact yellow above is used
    # 4.2/7 non-inverted rating = 0.6 score = yellow color
    # scores below this threshold blend with red; above with green
    MID_SCORE = 0.6


class UploadStages:
    UPLOAD = "upload"
    QUESTIONS = "questions"
    INSTRUCTORS = "instructors"
    FINISHED = "finished"


class UploadStageInfo:
    UPLOAD = {
        Attr.TITLE: "Upload CSV",
        Attr.STATUS: UploadStages.UPLOAD,
        Attr.PREVIOUS_STATUS: None,
        Attr.NEXT_STATUS: UploadStages.QUESTIONS,
    }
    QUESTIONS = {
        Attr.TITLE: "Merge questions",
        Attr.STATUS: UploadStages.QUESTIONS,
        Attr.PREVIOUS_STATUS: UploadStages.UPLOAD,
        Attr.NEXT_STATUS: UploadStages.INSTRUCTORS,
    }
    INSTRUCTORS = {
        Attr.TITLE: "Merge instructors",
        Attr.STATUS: UploadStages.INSTRUCTORS,
        Attr.PREVIOUS_STATUS: UploadStages.QUESTIONS,
        Attr.NEXT_STATUS: UploadStages.FINISHED,
    }
    FINISHED = {
        Attr.TITLE: "Upload finished!",
        Attr.STATUS: UploadStages.FINISHED,
        Attr.PREVIOUS_STATUS: UploadStages.INSTRUCTORS,
        Attr.NEXT_STATUS: None,
    }
