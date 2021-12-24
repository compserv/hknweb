from dto.rails.base import BaseDTO


class CourseDTO(BaseDTO):
    key = "course"

    class Attr(BaseDTO.Attr):
        SUFFIX = "suffix"
        PREFIX = "prefix"
        NAME = "name"
        DEPT_ID = "department_id"
        COURSE_NUMBER = "course_number"

    def __init__(self, json_data):
        super().__init__(json_data)

        self.name = json_data[self.Attr.NAME] or ""
        self.number = "{prefix}{number}{suffix}".format(
            prefix=json_data[self.Attr.PREFIX] or "",
            number=json_data[self.Attr.COURSE_NUMBER],
            suffix=json_data[self.Attr.SUFFIX] or "",
        )

        self.dept_id = json_data[self.Attr.DEPT_ID]
