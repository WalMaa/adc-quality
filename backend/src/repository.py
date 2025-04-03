from pymongo import MongoClient


MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "llm_dispatch"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
batches_collection = db["message_batches"]