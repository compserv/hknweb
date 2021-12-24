from dto.django.base import BaseModel


class ICSR(BaseModel):
    class Attr(BaseModel.Attr):
        ICSR_COURSE = "icsr_course"
        ICSR_DEPARTMENT = "icsr_department"
        ICSR_INSTRUCTOR = "icsr_instructor"
        ICSR_SEMESTER = "icsr_semester"
        FIRST_NAME = "first_name"
        LAST_NAME = "last_name"
        COURSE_NUMBER = "course_number"
        SECTION_NUMBER = "section_number"
        INSTRUCTOR_TYPE = "instructor_type"

    def __init__(
        self,
        instructor_dto,
        course_dto,
        instructorship_dto,
        klass_dto,
        course,
        department,
        instructor,
        semester,
    ):
        super().__init__()

        self.data = {
            self.Attr.ICSR_COURSE: course.remote_id,
            self.Attr.ICSR_DEPARTMENT: department.remote_id,
            self.Attr.ICSR_INSTRUCTOR: instructor.remote_id,
            self.Attr.ICSR_SEMESTER: semester.remote_id,
            self.Attr.FIRST_NAME: instructor_dto.first_name,
            self.Attr.LAST_NAME: instructor_dto.last_name,
            self.Attr.COURSE_NUMBER: course_dto.number,
            self.Attr.SECTION_NUMBER: klass_dto.section,
            self.Attr.INSTRUCTOR_TYPE: "Teaching Assistant" if instructorship_dto.ta else "Professor",
        }
