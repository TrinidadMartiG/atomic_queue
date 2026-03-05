from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    task_type: str
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskResponse(BaseModel):
    id: UUID
    task_type: str
    payload: dict[str, Any]
    status: str
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    worker_id: str | None
    result: dict[str, Any] | None
    error: str | None
