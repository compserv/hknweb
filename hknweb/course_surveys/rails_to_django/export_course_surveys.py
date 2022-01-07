import sys, json, time, pickle, os

from pprint import pprint
from collections import defaultdict

import requests
from requests.auth import HTTPBasicAuth

from dto import DJANGO, DJANGO_DTOS, RAILS_DTOS


FNAME = "course_surveys_data.json"
WEBSITE_BASE_URL = "http://localhost:3000/academics/api/"
AUTHENTICATION = HTTPBasicAuth()


def main():
    command = "upload"
    if len(sys.argv) > 1:
        command = sys.argv[1]

    if command not in FN_MAPPINGS:
        print(
            "Command not recognized. Try one of: \n- {}".format(
                "\n- ".join(FN_MAPPINGS.keys())
            )
        )
    else:
        FN_MAPPINGS[command]()


def load_data():
    with open(FNAME, "r", encoding="utf8") as f:
        data = json.load(f)

    return data


def data_to_rails_dtos(data):
    output_dtos = dict()
    for model_dto in RAILS_DTOS:
        json_models = data[model_dto.key]

        output_model_dtos = dict()
        for json_model in json_models:
            output_model_dto = model_dto(json_model)
            output_model_dtos[output_model_dto.id] = output_model_dto

        output_dtos[model_dto.key] = output_model_dtos

        print(model_dto.key, len(json_models))
        pprint(json_model)
        pprint(output_model_dto)
        print()

    return output_dtos


def print_update(i, n, start_time, text="Finished"):
    i = i + 1

    time_spent = time.time() - start_time
    time_left = (time_spent / i) * (n - i)
    h = int(time_left // 3600)
    m = int((time_left % 3600) // 60)
    s = int((time_left % 60))

    print(
        "%s %i / %i. Time remaining: %02d:%02d:%02d\r" % (text, i, n, h, m, s),
        flush=True,
        end="",
    )


class ModelUpload:
    TEMP_FILE_PATH = "model_upload.pt"

    def __init__(self, rails_dtos):
        if os.path.exists(self.TEMP_FILE_PATH):
            print("Continuing from last checkpoint")

            with open(self.TEMP_FILE_PATH, "rb") as f:
                _self = pickle.load(f)

            self.rails_dtos = _self.rails_dtos
            self.r2d = _self.r2d
            self.status = _self.status
            self.i = _self.i
        else:
            self.rails_dtos = rails_dtos
            self.r2d = defaultdict(dict)  # rails id to django model mappings
            self.status = 0
            self.i = 0

    def upload_models(self):
        try:
            if self.status < 1:
                print("Uploading departments...")
                self._upload_departments()
                self.status += 1
                self.i = 0

            if self.status < 2:
                print("Uploading instructors...")
                self._upload_instructors()
                self.status += 1
                self.i = 0

            if self.status < 3:
                print("Uploading semesters...")
                self._upload_semesters()
                self.status += 1
                self.i = 0

            if self.status < 4:
                print("Uploading courses and ICSRs...")
                self._upload_icsrs_courses()
                self.status += 1
                self.i = 0

            if self.status < 5:
                print("Uploading questions, surveys, and ratings...")
                self._upload_surveys_questions_ratings()
                self.status += 1
                self.i = 0

        except Exception as e:
            print()
            print(e)

            self.save()

    def save(self):
        with open(self.TEMP_FILE_PATH, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    def _upload_departments(self):
        department_dtos = self.rails_dtos["department"].values()
        for i, department_dto in enumerate(department_dtos):
            if self.i > i:
                continue

            self.i = i

            department = DJANGO.Department(department_dto)
            department.upload(WEBSITE_BASE_URL, AUTHENTICATION)

            self.r2d["department"][department_dto.id] = department

    def _upload_instructors(self):
        start_time = time.time()

        instructor_dtos = self.rails_dtos["instructor"].values()
        for i, instructor_dto in enumerate(instructor_dtos):
            if self.i > i:
                continue

            self.i = i

            instructor = DJANGO.Instructor(instructor_dto)
            instructor.upload(WEBSITE_BASE_URL, AUTHENTICATION)

            self.r2d["instructor"][instructor_dto.id] = instructor

            print_update(i, len(instructor_dtos), start_time)
        print()

    def _upload_semesters(self):
        klass_dtos = self.rails_dtos["klass"].values()
        for i, klass_dto in enumerate(klass_dtos):
            if self.i > i:
                continue

            self.i = i

            if klass_dto.semester in self.r2d["semester"]:
                continue

            semester = DJANGO.Semester(klass_dto)
            semester.upload(WEBSITE_BASE_URL, AUTHENTICATION)

            self.r2d["semester"][klass_dto.semester] = semester

    def _upload_icsrs_courses(self):
        start_time = time.time()

        instructorship_dtos = self.rails_dtos["instructorship"].values()
        for i, instructorship_dto in enumerate(instructorship_dtos):
            if self.i > i:
                continue

            self.i = i

            klass_dto = self.rails_dtos["klass"][instructorship_dto.klass_id]
            instructor_dto = self.rails_dtos["instructor"][
                instructorship_dto.instructor_id
            ]
            course_dto = self.rails_dtos["course"][klass_dto.course_id]

            course = self._get_or_upload_course(course_dto)
            department = self.r2d["department"][course_dto.dept_id]
            instructor = self.r2d["instructor"][instructor_dto.id]
            semester = self.r2d["semester"][klass_dto.semester]

            icsr = DJANGO.ICSR(
                instructor_dto,
                course_dto,
                instructorship_dto,
                klass_dto,
                course,
                department,
                instructor,
                semester,
            )
            icsr.upload(WEBSITE_BASE_URL, AUTHENTICATION)

            self.r2d["icsr"][instructorship_dto.id] = icsr

            print_update(i, len(instructorship_dtos), start_time)
        print()

    def _upload_surveys_questions_ratings(self):
        start_time = time.time()

        survey_answer_dtos = self.rails_dtos["survey_answer"].values()
        for i, survey_answer_dto in enumerate(survey_answer_dtos):
            if self.i > i:
                continue

            self.i = i

            instructorship_dto = self.rails_dtos["instructorship"][
                survey_answer_dto.instructorship_id
            ]
            survey_question_dto = self.rails_dtos["survey_question"][
                survey_answer_dto.survey_question_id
            ]

            icsr = self.r2d["icsr"][instructorship_dto.id]

            survey = DJANGO.Survey(survey_answer_dto, instructorship_dto, icsr)
            survey.upload(WEBSITE_BASE_URL, AUTHENTICATION)

            question = self._get_or_upload_question(survey_question_dto)

            rating = DJANGO.Rating(
                survey_answer_dto,
                survey_question_dto,
                survey,
                question,
            )
            rating.upload(WEBSITE_BASE_URL, AUTHENTICATION)

            print_update(i, len(survey_answer_dtos), start_time)
        print()

    def _get_or_upload_course(self, course_dto):
        if course_dto.id in self.r2d["course"]:
            return self.r2d["course"][course_dto.id]

        course = DJANGO.Course()
        course.upload(WEBSITE_BASE_URL, AUTHENTICATION)
        self.r2d["course"][course_dto.id] = course

        return course

    def _get_or_upload_question(self, survey_question_dto):
        if survey_question_dto.id in self.r2d["question"]:
            return self.r2d["question"][survey_question_dto.id]

        question = DJANGO.Question()
        question.upload(WEBSITE_BASE_URL, AUTHENTICATION)
        self.r2d["question"][survey_question_dto.id] = question

        return question


def upload_rails_data():
    if os.path.exists(ModelUpload.TEMP_FILE_PATH):
        ModelUpload(None).upload_models()
    else:
        data = load_data()
        rails_dtos = data_to_rails_dtos(data)
        ModelUpload(rails_dtos).upload_models()


def clear_course_surveys_db():
    for d in DJANGO_DTOS:
        print("Clearing {model_type} models...".format(model_type=d.__name__))

        url = WEBSITE_BASE_URL + d.api_url
        response = requests.get(url, auth=AUTHENTICATION)

        data = json.loads(response.content)
        for d in data:
            response = requests.delete(d["url"], auth=AUTHENTICATION)
            assert response.ok


def fill_missing_instructor_first_names():
    data = ModelUpload(None)

    instructorship_dtos = data.rails_dtos["instructorship"].values()
    for instructorship_dto in instructorship_dtos:
        instructor_dto = data.rails_dtos["instructor"][instructorship_dto.instructor_id]
        if not instructor_dto.first_name:
            instructor_dto.first_name = "MISSING_FIRST_NAME"

    data.save()


def combine_surveys():
    url = WEBSITE_BASE_URL + DJANGO.ICSR.api_url
    icsrs_response = requests.get(url, auth=AUTHENTICATION)
    assert icsrs_response.ok, icsrs_response.content
    icsrs_response = json.loads(icsrs_response.content)
    icsrs = icsrs_response["results"]

    i = 0
    start_time = time.time()
    while True:
        for icsr in icsrs:
            surveys = icsr["survey_icsr"]
            if len(surveys) != 0:
                base_survey_url = surveys[0]["url"].replace("http", "https")

                for survey in surveys[1:]:
                    survey_url = survey["url"].replace("http", "https")
                    ratings = survey["rating_survey"]

                    for rating in ratings:
                        rating_url = rating["url"].replace("http", "https")
                        data = {
                            "rating_survey": base_survey_url,
                        }
                        redirect_rating_response = requests.patch(
                            rating_url, auth=AUTHENTICATION, data=data
                        )
                        assert (
                            redirect_rating_response.ok
                        ), redirect_rating_response.content

                    delete_survey_response = requests.delete(
                        survey_url, auth=AUTHENTICATION
                    )
                    assert delete_survey_response.ok, delete_survey_response.content

            print_update(i, icsrs_response["count"], start_time, "Processing icsr")
            i += 1

        if not icsrs_response["next"]:
            break

        url = icsrs_response["next"].replace("http", "https")
        icsrs_response = requests.get(url, auth=AUTHENTICATION)
        assert icsrs_response.ok, icsrs_response.content
        icsrs_response = json.loads(icsrs_response.content)
        icsrs = icsrs_response["results"]
    print()


FN_MAPPINGS = {
    "upload": upload_rails_data,
    "clear": clear_course_surveys_db,
    "fill_first": fill_missing_instructor_first_names,
    "combine_surveys": combine_surveys,
}

if __name__ == "__main__":
    main()
