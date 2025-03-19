from fastapi import APIRouter, Depends, HTTPException, FastAPI
import uuid

from backend.app.models import BatchStatus, MessageBatch, MessageResponse

router = APIRouter(prefix="/messages")

# 1. Submit a new message batch
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



# 3. Check message batch status
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
    
# 4. Retrieve responses for a message batch
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
    
# 5. List all processed batches
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
    