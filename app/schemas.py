from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class StatusItem(str, Enum):
    TODO = "todo"
    INPROGRESS = "in-progress"
    DONE = "done"



class TaskCreate(BaseModel):
    description: str


class TaskUpdate(BaseModel):
    description: str | None = None
    status: StatusItem | None = None


class TaskResponse(BaseModel):
    id: int
    description: str
    status: StatusItem
    created_at: datetime
    updated_at: datetime