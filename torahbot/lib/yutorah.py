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
        return data["response"]["docs"]
