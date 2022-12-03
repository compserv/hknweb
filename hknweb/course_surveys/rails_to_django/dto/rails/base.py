class BaseDTO:
    key = None

    class Attr:
        ID = "id"
        URL = "url"

    def __init__(self, json_data):
        self.id = json_data[self.Attr.ID]

    def __repr__(self):
        return "BaseDTO(id={id})".format(id=self.id)
