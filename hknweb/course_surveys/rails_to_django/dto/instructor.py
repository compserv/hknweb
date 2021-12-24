from dto.base import BaseDTO


class InstructorDTO(BaseDTO):
    key = "instructor"

    class Attr(BaseDTO.Attr):
        FIRST_NAME = "first_name"
        LAST_NAME = "last_name"
        PRIVATE = "private"
        INSTRUCTOR_ID = "instructor_id"

    def __init__(self, json_data):
        super().__init__(json_data)

        self.first_name = json_data[self.Attr.FIRST_NAME]
        self.last_name = json_data[self.Attr.LAST_NAME]
        self.private = json_data[self.Attr.PRIVATE]

    def __repr__(self):
        return "InstructorDTO(id={id}, first_name={first_name}, last_name={last_name}, private={private})".format(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            private=self.private,
        )
