import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

from dto import RAILS_DTOS, DJANGO


FNAME = "course_surveys_data.json"
WEBSITE_BASE_URL = "http://localhost:3000/academics/api/"
AUTHENTICATION = HTTPBasicAuth()


with open(FNAME, "r", encoding="utf8") as f:
    data = json.load(f)


output_dtos = dict()
for model_dto in RAILS_DTOS:
    json_models = data[model_dto.key]

    output_model_dtos = dict()
    for json_model in json_models:
        output_model_dto = model_dto(json_model)
        # output_model_dto.upload(WEBSITE_BASE_URL, AUTHENTICATION)
        output_model_dtos[output_model_dto.id] = output_model_dto

    output_dtos[model_dto.key] = output_model_dtos

    print(model_dto.key, len(json_models))
    pprint(json_model)
    pprint(output_model_dto)
    input()



