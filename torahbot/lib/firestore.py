import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from configparser import SectionProxy
from google.cloud.firestore_v1.collection import CollectionReference


class FireStoreClient:

    def __init__(self, config: SectionProxy):
        # Use the application default credentials
        if not len(firebase_admin._apps):
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
                'projectId': config["FIRESTORE_PROJECT_ID"],
            })

        db = firestore.client()
        self._shiur_collection: CollectionReference = db.collection(config["FIRESTORE_SHIURIM_COLLECTION"])

    def shiur_exists(self, shiur_id: int) -> bool:
        return self._shiur_collection.document(str(shiur_id)).get().exists

    def insert_shiur(self, shiur_id: int, teacher_id: int, teacher_name: str, shiur_date: str, shiur_url: str, shiur_title: str) -> None:
        doc_ref = self._shiur_collection.document(str(shiur_id))
        doc_ref.set({
            "teacher_id": teacher_id,
            "teacher_name": teacher_name,
            "shiur_date": shiur_date,
            "shiur_url": shiur_url,
            "shiur_title": shiur_title
        })
