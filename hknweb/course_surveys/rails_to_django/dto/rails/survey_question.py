from dto.rails.base import BaseDTO


class SurveyQuestionDTO(BaseDTO):
    key = "survey_question"

    class Attr(BaseDTO.Attr):
        TEXT = "text"
        INVERTED = "inverted"
        MAX = "max"

    def __init__(self, json_data):
        super().__init__(json_data)

        self.text = json_data[self.Attr.TEXT]
        self.inverted = json_data[self.Attr.INVERTED]
        self.max = json_data[self.Attr.MAX]

    def __repr__(self):
        return "SurveyQuestionDTO(id={id}, text={text}, inverted={inverted}, max={max})".format(
            id=self.id,
            text=self.text,
            inverted=self.inverted,
            max=self.max,
        )
