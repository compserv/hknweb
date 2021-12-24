from dto.django.base import BaseModel


class Instructor(BaseModel):
    api_url = "instructors/"

    class Attr(BaseModel.Attr):
        INSTRUCTOR_ID = "instructor_id"
        ID = "instructor_id"

    def __init__(self, instructor_dto):
        super().__init__()

        self.data = {
            self.Attr.INSTRUCTOR_ID: instructor_dto.id,
        }
