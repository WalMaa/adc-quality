from pydantic import BaseModel
from typing import List, Dict, Optional

class Message(BaseModel):
    role: str
    content: str

class MessageBatch(BaseModel):
    messages: List[Message]
    llms: List[str]

class MessageResponse(BaseModel):
    batch_id: str
    status: str
    processed_at: Optional[str] = None
    responses: Optional[List[Dict[str, str]]] = None

class BatchStatus(BaseModel):
    batch_id: str
    status: str
    processed_at: Optional[str] = None