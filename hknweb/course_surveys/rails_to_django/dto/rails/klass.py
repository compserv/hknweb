from dto.rails.base import BaseDTO


class KlassDTO(BaseDTO):
    key = "klass"

    class Attr(BaseDTO.Attr):
        COURSE_ID = "course_id"
        SEMESTER = "semester"
        NUM_STUDENTS = "num_students"
        SECTION = "section"

    def __init__(self, json_data):
        super().__init__(json_data)

        self.course_id = json_data[self.Attr.COURSE_ID]
        self.semester = json_data[self.Attr.SEMESTER]
        self.num_students = json_data[self.Attr.NUM_STUDENTS]
        self.section = json_data[self.Attr.SECTION]

    def __repr__(self):
        return "KlassDTO(id={id}, semester={semester}, num_students={num_students}, section={section})".format(
            id=self.id,
            semester=self.semester,
            num_students=self.num_students,
            section=self.section,
        )
