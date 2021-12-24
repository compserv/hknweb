from dto.django.base import BaseModel


class Rating(BaseModel):
    class Attr(BaseModel.Attr):
        RATING_QUESTION = "rating_question"
        RATING_SURVEY = "rating_survey"
        QUESTION_TEXT = "question_text"
        INVERTED = "inverted"
        RANGE_MAX = "range_max"
        RATING_VALUE = "rating_value"

    def __init__(self, survey_answer_dto, survey_question_dto, survey):
        super().__init__()

        self.data = {
            self.Attr.RATING_QUESTION: survey_question_dto.remote_id,
            self.Attr.RATING_SURVEY: survey.remote_id,
            self.Attr.QUESTION_TEXT: survey_question_dto.text,
            self.Attr.INVERTED: survey_question_dto.inverted,
            self.Attr.RANGE_MAX: survey_question_dto.max,
            self.Attr.RATING_VALUE: survey_answer_dto.mean,
        }
