import requests
import json
from configparser import SectionProxy
import logging
from bs4 import BeautifulSoup
from random import choice


class YUTorahClient:

    def __init__(self, config: SectionProxy):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger("YUTorahClient")

        self.url_template = config["SHIUR_LOOKUP_URL_TEMPLATE"]
        self.proxy_rotator_url = config["PROXY_ROTATOR_URL"]
        self.yu_request_timeout = int(config["YUZMANIM_REQUEST_TIMEOUT"])
        self.yu_request_tries = int(config["YUZMANIM_REQUEST_TRIES"])

    def get_shiurim_by_teacher(self, teacher_id, page=1):
        url = self.url_template.format(
            page,
            teacher_id
        )
        self.logger.info("getting shiur data: {}".format(url))
        response = requests.get(
            url=url
        )
        data = json.loads(response.text)
        self.logger.info("shiur data: {}".format(response.text))
        return data["response"]["docs"]
