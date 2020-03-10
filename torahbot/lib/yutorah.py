import requests
import json
from configparser import SectionProxy


class YUTorahClient:

    def __init__(self, config: SectionProxy):
        self.url_template = config["SHIUR_LOOKUP_URL_TEMPLATE"]
        self.proxy_rotator_url = config["PROXY_ROTATOR_URL"]
        self.yu_request_timeout = int(config["YUZMANIM_REQUEST_TIMEOUT"])

    def _proxy_generator(self):
        data = json.loads(requests.get(self.proxy_rotator_url).text)
        return {"https": data["proxy"]}

    def get_shiurim_by_teacher(self, teacher_id, page=1):
        url = self.url_template.format(
            page,
            teacher_id
        )
        response = requests.get(
            url=url,
            proxies=self._proxy_generator(),
            timeout=self.yu_request_timeout
        )
        data = json.loads(response.text)
        return data["response"]["docs"]
