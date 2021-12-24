from dto.base import BaseDTO


class SurveyAnswerDTO(BaseDTO):
    key = "survey_answer"

    class Attr(BaseDTO.Attr):
        SURVEY_QUESTION_ID = "survey_question_id"
        INSTRUCTORSHIP_ID = "instructorship_id"
        MEAN = "mean"
        NUM_RESPONSES = "num_responses"
        ENROLLMENT = "enrollment"

    def __init__(self, json_data):
        super().__init__(json_data)

        self.survey_question_id = json_data[self.Attr.SURVEY_QUESTION_ID]
        self.instructorship_id = json_data[self.Attr.INSTRUCTORSHIP_ID]
        self.mean = json_data[self.Attr.MEAN]
        self.num_responses = json_data[self.Attr.NUM_RESPONSES]
        self.enrollment = json_data[self.Attr.ENROLLMENT]

    def __repr__(self):
        return "SurveyAnswerDTO(id={id}, mean={mean}, num_responses={num_responses}, enrollment={enrollment})".format(
            id=self.id,
            mean=self.mean,
            num_responses=self.num_responses,
            enrollment=self.enrollment,
        )
