from dto.rails.base import BaseDTO


class DepartmentDTO(BaseDTO):
    key = "department"
    api_url = "departments/"

    class Attr(BaseDTO.Attr):
        ABBR = "abbr"
        NAME = "name"

    def __init__(self, json_data):
        super().__init__(json_data)

        self.abbr = json_data[self.Attr.ABBR]
        self.name = json_data[self.Attr.NAME]

    def __repr__(self):
        return "DepartmentDTO(id={id}, abbr={abbr}, name={name})".format(
            id=self.id,
            abbr=self.abbr,
            name=self.name,
        )
