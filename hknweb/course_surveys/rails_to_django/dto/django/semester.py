from dto.django.base import BaseModel


class Semester(BaseModel):
    class Attr(BaseModel.Attr):
        YEAR = "year"
        YEAR_SECTION = "year_section"
    
    SECTION_MAPPING = {
        "1": "Sp",
        "2": "Su",
        "3": "Fa",
    }

    def __init__(self, klass_dto):
        super().__init__()

        self.data = {
            self.Attr.YEAR: klass_dto.semester[:4],
            self.Attr.YEAR_SECTION: self.SECTION_MAPPING[klass_dto.semester[-1]],
        }
