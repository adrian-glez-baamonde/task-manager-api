from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class StatusItem(str, Enum):
    TODO = "todo"
    INPROGRESS = "in-progress"
    DONE = "done"



class TaskCreate(BaseModel):
    description: str
    category_id: int | None = None


class TaskUpdate(BaseModel):
    description: str | None = None
    status: StatusItem | None = None
    category_id: int | None = None


class TaskResponse(BaseModel):
    id: int
    description: str
    status: StatusItem
    category_id: int | None = None
    created_at: datetime
    updated_at: datetime


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str