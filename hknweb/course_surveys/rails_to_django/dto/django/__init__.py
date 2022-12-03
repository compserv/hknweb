from dto.django.course import Course
from dto.django.department import Department
from dto.django.icsr import ICSR
from dto.django.instructor import Instructor
from dto.django.question import Question
from dto.django.rating import Rating
from dto.django.semester import Semester
from dto.django.survey import Survey


class DJANGO:
    Course = Course
    Department = Department
    ICSR = ICSR
    Instructor = Instructor
    Question = Question
    Rating = Rating
    Semester = Semester
    Survey = Survey


# This order is important for mass deletion!
DJANGO_DTOS = [
    Rating,
    Question,
    Survey,
    ICSR,
    Course,
    Department,
    Instructor,
    Semester,
]
