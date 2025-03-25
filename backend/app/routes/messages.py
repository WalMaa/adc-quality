from bson import ObjectId
from typing import List
from fastapi import APIRouter, HTTPException

from src.models import MessageRequest
from src.db import get_database

router = APIRouter(prefix="/messages")

# Save a new user message
@router.post("/user")
async def save_user_message(req: MessageRequest):
    db = get_database()
    user_messages = db.get_collection("user_messages")
    result = user_messages.insert_one({"content": req.message})
    return {"id": str(result.inserted_id), "message": "User message saved"}

# Save a new system message
@router.post("/system")
async def save_system_message(req: MessageRequest):
    db = get_database()
    system_messages = db.get_collection("system_messages")
    result = system_messages.insert_one({"content": req.message})
    return {"id": str(result.inserted_id), "message": "System message saved"}

# List all user messages
@router.get("/user")
async def list_user_messages():
    db = get_database()
    user_messages = db.get_collection("user_messages")
    messages = list(user_messages.find())
    
    # Convert ObjectId to string for JSON serialization
    for message in messages:
        message["_id"] = str(message["_id"])
    
    return messages

# List all system messages
@router.get("/system")
async def list_system_messages():
    db = get_database()
    system_messages = db.get_collection("system_messages")
    messages = list(system_messages.find())
    
    # Convert ObjectId to string for JSON serialization
    for message in messages:
        message["_id"] = str(message["_id"])
    
    return messages

# Retrieve a user message
@router.get("/user/{message_id}")
async def get_user_message(message_id: str):
    try:
        db = get_database()
        user_messages = db.get_collection("user_messages")
        message = user_messages.find_one({"_id": ObjectId(message_id)})
        
        if message:
            message["_id"] = str(message["_id"])
            return message
        
        raise HTTPException(status_code=404, detail="User message not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid message ID format: {str(e)}")

# Retrieve a system message
@router.get("/system/{message_id}")
async def get_system_message(message_id: str):
    try:
        db = get_database()
        system_messages = db.get_collection("system_messages")
        message = system_messages.find_one({"_id": ObjectId(message_id)})
        
        if message:
            message["_id"] = str(message["_id"])
            return message
        
        raise HTTPException(status_code=404, detail="System message not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid message ID format: {str(e)}")

# Delete a user message
@router.delete("/user/{message_id}")
async def delete_user_message(message_id: str):
    try:
        db = get_database()
        user_messages = db.get_collection("user_messages")
        result = user_messages.delete_one({"_id": ObjectId(message_id)})
        
        if result.deleted_count:
            return {"message": f"User message {message_id} deleted"}
        
        raise HTTPException(status_code=404, detail="User message not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid message ID format: {str(e)}")

# Delete a system message
@router.delete("/system/{message_id}")
async def delete_system_message(message_id: str):
    try:
        db = get_database()
        system_messages = db.get_collection("system_messages")
        result = system_messages.delete_one({"_id": ObjectId(message_id)})
        
        if result.deleted_count:
            return {"message": f"System message {message_id} deleted"}
        
        raise HTTPException(status_code=404, detail="System message not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid message ID format: {str(e)}")