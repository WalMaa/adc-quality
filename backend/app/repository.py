from pymongo import MongoClient
from typing import List, Dict, Optional
import datetime
import uuid

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "llm_dispatch"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
batches_collection = db["message_batches"]