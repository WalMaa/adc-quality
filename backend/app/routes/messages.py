from fastapi import APIRouter, Depends, HTTPException, FastAPI
import uuid

from backend.app.models import BatchStatus, MessageBatch, MessageResponse

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


# Submit a new message batch
@router.post("/", response_model=BatchStatus)
async def submit_message_batch(batch: MessageBatch):
    batch_id = str(uuid.uuid4())
    if not set(batch.llms).issubset(set(llms_available)):
        raise HTTPException(status_code=400, detail="One or more LLMs are not available.")

    message_batches[batch_id] = {
        "status": "processing",
        "messages": batch.messages,
        "llms": batch.llms,
        "processed_at": None,
        "responses": []
    }
    return {"batch_id": batch_id, "status": "processing"}



# Check message batch status
@router.get("/messages/{batch_id}/status", response_model=BatchStatus)
async def get_batch_status(batch_id: str):
    if batch_id not in message_batches:
        raise HTTPException(status_code=404, detail="Batch not found")
    batch = message_batches[batch_id]
    return {
        "batch_id": batch_id,
        "status": batch["status"],
        "processed_at": batch["processed_at"]
    }
    
# Retrieve responses for a message batch
@router.get("/messages/{batch_id}/responses", response_model=MessageResponse)
async def get_batch_responses(batch_id: str):
    if batch_id not in message_batches:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    batch = message_batches[batch_id]
    return {
        "batch_id": batch_id,
        "status": batch["status"],
        "processed_at": batch["processed_at"],
        "responses": batch["responses"]
    }
    
# List all processed batches
@router.get("/messages")
async def list_message_batches():
    return {
        "batches": [
            {
                "batch_id": batch_id,
                "status": data["status"],
                "processed_at": data["processed_at"]
            } for batch_id, data in message_batches.items()
        ]
    }
    