from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 compatibility
