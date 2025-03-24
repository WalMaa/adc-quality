from fastapi import APIRouter
from src.models import MessageRequest
from src.db import get_database
from bson import ObjectId

router = APIRouter(prefix="/messages")

# Save a new user message
@router.post("/user")
async def save_user_message(req: MessageRequest):
    db = get_database()
    user_messages = db.get_collection("user_messages")
    user_messages.insert_one({"message": req.message})
    return "User message saved"

# Save a new system message
@router.post("/system")
async def save_system_message(req: MessageRequest):
    db = get_database()
    print("DB: ", db)
    system_messages = db.get_collection("system_messages")
    system_messages.insert_one({"message": req.message})
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