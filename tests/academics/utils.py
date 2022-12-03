from datetime import datetime

from django.contrib.auth.models import User, Group

from hknweb.academics.models import (
    Course,
    Department,
    Instructor,
    Semester,
    Question,
    Rating,
    Survey,
    ICSR,
)


class ModelFactory:
    @staticmethod
    def create_course(**kwargs):
        return Course.objects.create(**kwargs)

    @staticmethod
    def create_department(**kwargs):
        default_kwargs = {
            "name": "default name",
            "abbr": "default abbr",
        }
        kwargs = {**default_kwargs, **kwargs}
        return Department.objects.create(**kwargs)

    @staticmethod
    def create_instructor(instructor_id, **kwargs):
        required_kwargs = {
            "instructor_id": instructor_id,
        }
        kwargs = {**required_kwargs, **kwargs}
        return Instructor.objects.create(**kwargs)

    @staticmethod
    def create_semester(**kwargs):
        default_kwargs = {
            "year": datetime.now().year,
            "year_section": Semester.SPRING,
        }
        kwargs = {**default_kwargs, **kwargs}
        return Semester.objects.create(**kwargs)

    @staticmethod
    def create_question(**kwargs):
        return Question.objects.create(**kwargs)

    @staticmethod
    def create_rating(rating_question, rating_survey, **kwargs):
        required_kwargs = {
            "rating_question": rating_question,
            "rating_survey": rating_survey,
        }
        default_kwargs = {
            "question_text": "default question_text",
            "rating_value": 4.5,
        }
        kwargs = {
            **required_kwargs,
            **default_kwargs,
            **kwargs,
        }
        return Rating.objects.create(**kwargs)

    @staticmethod
    def create_default_rating(**kwargs):
        rating_question = ModelFactory.create_question(**kwargs)
        rating_survey = ModelFactory.create_default_survey(**kwargs)

        return ModelFactory.create_rating(
            rating_question=rating_question,
            rating_survey=rating_survey,
            **kwargs,
        )

    @staticmethod
    def create_survey(survey_icsr, **kwargs):
        required_kwargs = {
            "survey_icsr": survey_icsr,
        }
        default_kwargs = {
            "num_students": 100,
            "response_count": 50,
        }
        kwargs = {
            **required_kwargs,
            **default_kwargs,
            **kwargs,
        }
        return Survey.objects.create(**kwargs)

    @staticmethod
    def create_default_survey(**kwargs):
        survey_icsr = ModelFactory.create_default_icsr(**kwargs)

        return ModelFactory.create_survey(survey_icsr=survey_icsr, **kwargs)

    @staticmethod
    def create_icsr(
        icsr_course, icsr_department, icsr_instructor, icsr_semester, **kwargs
    ):
        required_kwargs = {
            "icsr_course": icsr_course,
            "icsr_department": icsr_department,
            "icsr_instructor": icsr_instructor,
            "icsr_semester": icsr_semester,
        }
        default_kwargs = {
            "first_name": "default first_name",
            "last_name": "default last_name",
            "course_number": "default course_number",
            "course_name": "default course_name",
            "section_number": "default section_number",
            "instructor_type": "default instructor_type",
        }
        kwargs = {
            **required_kwargs,
            **default_kwargs,
            **kwargs,
        }
        return ICSR.objects.create(**kwargs)

    @staticmethod
    def create_default_icsr(**kwargs):
        icsr_course = ModelFactory.create_course()
        icsr_department = ModelFactory.create_department()
        icsr_instructor = ModelFactory.create_instructor("default instructor_id")
        icsr_semester = ModelFactory.create_semester()

        return ModelFactory.create_icsr(
            icsr_course=icsr_course,
            icsr_department=icsr_department,
            icsr_instructor=icsr_instructor,
            icsr_semester=icsr_semester,
            **kwargs,
        )

    @staticmethod
    def create_user(**kwargs):
        default_kwargs = {
            "username": "default username",
        }
        kwargs = {**default_kwargs, **kwargs}
        return User.objects.create(**kwargs)


def login_user(test_cls):
    user = ModelFactory.create_user()
    password = "custom password"
    user.set_password(password)
    user.save()

    group = Group(name="officer")
    group.save()
    group.user_set.add(user)
    group.save()

    test_cls.client.login(username=user.username, password=password)
