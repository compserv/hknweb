from dto.django.base import BaseModel


class Survey(BaseModel):
    class Attr(BaseModel.Attr):
        SURVEY_ICSR = "survey_icsr"
        NUM_STUDENTS = "num_students"
        RESPONSE_COUNT = "response_count"
        IS_PRIVATE = "is_private"

    def __init__(self, survey_answer_dto, instructorship_dto, icsr):
        super().__init__()

        self.data = {
            self.Attr.SURVEY_ICSR: icsr.remote_id,
            self.Attr.NUM_STUDENTS: survey_answer_dto.enrollment,
            self.Attr.RESPONSE_COUNT: survey_answer_dto.num_responses,
            self.Attr.IS_PRIVATE: instructorship_dto.hidden,
        }
