import requests
import json


class BaseModel:
    api_url = None

    class Attr:
        ID = "id"
        URL = "url"

    def __init__(self):
        self.data = {}

    def upload(self, base_url, auth):
        url = base_url + self.api_url

        response = requests.post(url, data=self.data, auth=auth)
        assert response.ok, response.content

        content = json.loads(response.content)
        self.remote_id = content[self.Attr.ID]
        self.remote_url = content[self.Attr.URL]
