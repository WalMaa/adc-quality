from fastapi import APIRouter

from backend.app.models 

router = APIRouter(prefix="/messages")

# Save a new user message
@router.post("/user")
async def save_user_message(message: str):
    # TODO: save user message to db
    return "User message saved"

# Save a new system message
@router.post("/system")
async def save_system_message(message: str):
    # TODO: save system message to db
    return "System message saved"

# List all user messages
@router.get("/user")
async def list_user_messages():
    #TODO: get user messages from db
    return ["User message 1", "User message 2"]

# List all system messages
@router.get("/system")
async def list_system_messages():
    #TODO: get system messages from db
    return ["System message 1", "System message 2"]

# Retrieve a user message
@router.get("/user/{message_id}")
async def get_user_message(message_id: int):
    #TODO: get user message from db
    return f"User message {message_id}"

# Retrieve a system message
@router.get("/system/{message_id}")
async def get_system_message(message_id: int):
    #TODO: get system message from db
    return f"System message {message_id}"

# Delete a user message
@router.delete("/user/{message_id}")
async def delete_user_message(message_id: int):
    #TODO: delete user message from db
    return f"User message {message_id} deleted"

# Delete a system message
@router.delete("/system/{message_id}")
async def delete_system_message(message_id: int):
    #TODO: delete system message from db
    return f"System message {message_id} deleted"