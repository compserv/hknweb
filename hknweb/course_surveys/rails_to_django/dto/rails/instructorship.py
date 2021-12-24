from dto.rails.base import BaseDTO


class InstructorshipDTO(BaseDTO):
    key = "instructorship"

    class Attr(BaseDTO.Attr):
        KLASS_ID = "klass_id"
        INSTRUCTOR_ID = "instructor_id"
        TA = "ta"
        HIDDEN = "hidden"

    def __init__(self, json_data):
        super().__init__(json_data)

        self.klass_id = json_data[self.Attr.KLASS_ID]
        self.instructor_id = json_data[self.Attr.INSTRUCTOR_ID]
        self.ta = json_data[self.Attr.TA]
        self.hidden = json_data[self.Attr.HIDDEN]

    def __repr__(self):
        return "InstructorshipDTO(id={id}, ta={ta}, hidden={hidden})".format(
            id=self.id,
            ta=self.ta,
            hidden=self.hidden,
        )
