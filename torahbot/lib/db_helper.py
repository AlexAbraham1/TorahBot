import pymongo
from pymongo.database import Database
from pymongo.collection import Collection
from configparser import SectionProxy
import logging


class MongoDBHelper:

    def __init__(self, config: SectionProxy):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger("MongoDBHelper")

        client: pymongo = pymongo.MongoClient(config["MONGO_CONNECTION_URI"])
        self._db: Database = client[config["MONGODB_DATABASE_NAME"]]
        self._shiur_collection_name: str = config["MONGODB_SHIURIM_COLLECTION"]

    def _get_shiur_collection(self) -> Collection:
        return self._db[self._shiur_collection_name]

    def shiur_exists(self, shiur_id: int) -> bool:
        collection = self._get_shiur_collection()
        return collection.count_documents({ 'shiur_id': shiur_id }, limit = 1) != 0

    def insert_shiur(self, shiur_id: int, teacher_id: int, teacher_name: str, shiur_date: str, shiur_url: str, shiur_title: str) -> None:
        collection = self._get_shiur_collection()
        document = {
            "shiur_id": shiur_id,
            "teacher_id": teacher_id,
            "teacher_name": teacher_name,
            "shiur_date": shiur_date,
            "shiur_url": shiur_url,
            "shiur_title": shiur_title
        }
        self.logger.info("inserting document into mongodb")
        self.logger.info("{}".format(document))
        collection.insert_one(document)
