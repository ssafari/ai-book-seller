from typing import Optional
from pydantic import BaseModel

class InvokeRequest(BaseModel):
    input_message: str
    thread_id: Optional[str] = None # For managing conversational state
