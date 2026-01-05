from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    priority: int

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    due_date: datetime
    priority: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
