from dto.django.base import BaseModel


class Department(BaseModel):
    api_url = "departments/"

    class Attr(BaseModel.Attr):
        NAME = "name"
        ABBR = "abbr"

    def __init__(self, department_dto):
        super().__init__()

        self.data = {
            self.Attr.NAME: department_dto.name,
            self.Attr.ABBR: department_dto.abbr,
        }
