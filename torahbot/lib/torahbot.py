from torahbot.lib.yutorah import YUTorahClient
from torahbot.lib.telegram import TelegramClient
from torahbot.lib.db_helper import MongoDBHelper

from datetime import datetime as dt
from time import sleep
import random
import logging
import requests
from io import BytesIO
from configparser import ConfigParser


class TorahBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger("TorahBot")

        config = ConfigParser()
        config.read("settings.cfg")

        self.mongo = MongoDBHelper(config["MONGODB"])
        self.yutorah_client = YUTorahClient(config["YUTORAH_CLIENT"])

        self.telegram_client = TelegramClient(config["TELEGRAM_CLIENT"])
        self.telegram_chat_id = int(config["MAIN"]["TELEGRAM_CHAT_ID"])

        self.teacher_ids = [int(x) for x in config["MAIN"]["YUTORAH_TEACHER_IDS"].split(",")]
        self.message_template_new_shiur = config["MAIN"]["MESSAGE_TEMPLATE_NEW_SHIUR"]
        self.yutorah_min_sleep = int(config["MAIN"]["YUTORAH_MIN_SLEEP"])
        self.yutorah_max_sleep = int(config["MAIN"]["YUTORAH_MAX_SLEEP"])

    def insert_shiur_to_db(self, db_record: dict):
        self.logger.info("inserting shiur into database")
        self.mongo.insert_shiur(
            shiur_id=db_record["shiur_id"],
            teacher_id=db_record["teacher_id"],
            teacher_name=db_record["teacher_name"],
            shiur_date=db_record["shiur_date"],
            shiur_url=db_record["shiur_url"],
            shiur_title=db_record["shiur_title"]
        )

    def send_telegram(self, db_record: dict):
        self.logger.info("sending telegram")
        self.telegram_client.send_text(
            chat_id=self.telegram_chat_id,
            text=self.message_template_new_shiur.format(
                teacher=db_record["teacher_name"],
                title=db_record["shiur_title"],
                date=dt.strptime(db_record["shiur_date"], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y - %I:%M %p")
            )
        )

        audio = BytesIO(requests.get(db_record["shiur_url"]).content)
        self.telegram_client.send_audio(
            chat_id=self.telegram_chat_id,
            audio=audio
        )

    def run_shiur_retrieval(self, teacher_id):
        shiurim = self.yutorah_client.get_shiurim_by_teacher(teacher_id=teacher_id)
        for shiur in shiurim:
            # since the client returns results sorted by date desc, we can break loop once we see a familiar shiur_id
            if self.mongo.shiur_exists(shiur["shiurid"]):
                break

            db_record = {
                "shiur_id": shiur["shiurid"],
                "teacher_id": shiur["teacherid"],
                "teacher_name": " ".join(shiur["teacherfullname"].split()).strip(),
                "shiur_date": shiur["shiurdatesubmitted"],
                "shiur_url": shiur["shiurdownloadurl"],
                "shiur_title": shiur["shiurtitle"]
            }
            self.logger.info("shiur retriaval: new db record - {}".format(db_record))
            self.send_telegram(db_record)
            self.insert_shiur_to_db(db_record)

    def start_shiur_retrieval(self):
        self.logger.info("starting shiur retrieval")
        while True:
            for teacher_id in self.teacher_ids:
                self.run_shiur_retrieval(teacher_id)
            sleep_time = random.randint(self.yutorah_min_sleep, self.yutorah_max_sleep)
            sleep(sleep_time)

    def run(self):
        try:
            self.start_shiur_retrieval()
        except KeyboardInterrupt as ki:
            logging.info("Good Bye!")
