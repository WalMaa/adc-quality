from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "llm_dispatch"

client = None
db = None
batches_collection = None


def init_db():
    global client, db, batches_collection
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    batches_collection = db["message_batches"]
