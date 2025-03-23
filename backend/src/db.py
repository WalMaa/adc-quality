from pymongo import MongoClient

# Global variable to hold the database connection
db = None

def get_database():
    return db

def init_db(mongo_uri="mongodb://root:pass@mongo:27017/"):
    """Initialize the database connection"""
    try:
        client = MongoClient(mongo_uri, connectTimeoutMS=5000, 
                            socketTimeoutMS=5000, serverSelectionTimeoutMS=5000)
        global db
        db = client["mydb"]
        client.admin.command('ping')
        print("Connected to MongoDB")
        
        create_collections()
        return client, db
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")
        return None, None
    
def create_collections():
    """Create collections if they don't exist"""
    collections = ["user_messages", "system_messages", "responses"]

    for collection_name in collections:
        # Check if the collection exists; if not, create it (MongoDB creates collections on insert if not exist)
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection {collection_name} created")
        else:
            print(f"Collection {collection_name} already exists")