import requests
import json
from configparser import SectionProxy


class YUTorahClient:

    def __init__(self, config: SectionProxy):
        self.url_template = config["SHIUR_LOOKUP_URL_TEMPLATE"]

    def get_shiurim_by_teacher(self, teacher_id, page=1):
        url = self.url_template.format(
            page,
            teacher_id
        )
        data = json.loads(requests.get(url).text)
        return data["response"]["docs"]
