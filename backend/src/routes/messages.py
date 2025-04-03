import sys
import importlib.util
from pathlib import Path
from fastapi import APIRouter
from bson import ObjectId

models_path = Path(__file__).resolve().parents[2] / "src" / "models.py"
spec_models = importlib.util.spec_from_file_location("models_module", models_path)
models_module = importlib.util.module_from_spec(spec_models)
sys.modules["models_module"] = models_module
spec_models.loader.exec_module(models_module)

db_path = Path(__file__).resolve().parents[2] / "src" / "db.py"
spec_db = importlib.util.spec_from_file_location("db_module", db_path)
db_module = importlib.util.module_from_spec(spec_db)
sys.modules["db_module"] = db_module
spec_db.loader.exec_module(db_module)

MessageRequest = models_module.MessageRequest
get_database = db_module.get_database

router = APIRouter(prefix="/messages")

# Save a new user message
@router.post("/user")
async def save_user_message(req: MessageRequest):
    db = get_database()
    print("Connected to DB:", db.name)
    user_messages = db.get_collection("user_messages")
    user_messages.insert_one({"message": req.message})
    return "User message saved"

@router.post("/system")
async def save_system_message(req: MessageRequest):
    db = get_database()
    system_messages = db.get_collection("system_messages")
    result = system_messages.insert_one({"message": req.message})
    print(f"Inserted document ID: {result.inserted_id}")
    return "System message saved"

# List all user messages -------
@router.get("/user")
async def list_user_messages():
    db = get_database()
    
    user_messages = db["user_messages"]
    items = list(user_messages.find())
    
    for item in items:
        item["_id"] = str(item["_id"])
    
    return items

# List all system messages --------------
@router.get("/system")
async def list_system_messages():
    db = get_database()
    system_messages = db["system_messages"]
    items = list(system_messages.find())
    
    for item in items:
        item["_id"] = str(item["_id"])
    return items


# Retrieve a user message
@router.get("/user/{message_id}")
async def get_user_message(message_id: str):
    db = get_database()
    user_messages = db["user_messages"]
    message = user_messages.find_one({"_id": ObjectId(message_id)})
    
    if message:
        message["_id"] = str(message["_id"])
        return message
    return {"error": "User message not found"}

# Retrieve a system message
@router.get("/system/{message_id}")
async def get_system_message(message_id: str):
    db = get_database()
    system_messages = db["system_messages"]
    message = system_messages.find_one({"_id": ObjectId(message_id)})
    
    if message:
        message["_id"] = str(message["_id"])
        return message
    return {"error": "System message not found"}

# Delete a user message
@router.delete("/user/{message_id}")
async def delete_user_message(message_id: str):
    db = get_database()
    user_messages = db["user_messages"]
    result = user_messages.delete_one({"_id": ObjectId(message_id)})
    
    if result.deleted_count == 1:
        return {"message": f"User message {message_id} deleted"}
    return {"error": "User message not found"}

# Delete a system message
@router.delete("/system/{message_id}")
async def delete_system_message(message_id: str):
    db = get_database()
    system_messages = db["system_messages"]
    result = system_messages.delete_one({"_id": ObjectId(message_id)})
    
    if result.deleted_count == 1:
        return {"message": f"System message {message_id} deleted"}
    return {"error": "System message not found"}