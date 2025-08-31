from typing import Any
from datetime import datetime
from pydantic import BaseModel


class AuditEvent(BaseModel):
    user: str
    action: str
    timestamp: datetime
    model: str
    record_id: Any
    changes: dict[str, Any]
