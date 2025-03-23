from pydantic import BaseModel
from typing import List, Dict, Optional

    
class PromptRequest(BaseModel):
    system_message: str
    user_message: str