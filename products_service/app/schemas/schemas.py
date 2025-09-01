from pydantic import BaseModel
from datetime import datetime
from typing import Any


class Message(BaseModel):
    message: str


class AuditEvent(BaseModel):
    user: str
    action: str
    timestamp: datetime
    model: str
    record_id: Any
    changes: dict[str, Any]
