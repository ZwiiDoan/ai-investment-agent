from pydantic import BaseModel
from typing import Optional, Dict

class Document(BaseModel):
    id: Optional[str] = None
    title: str
    text: str
    metadata: Optional[Dict] = None
