
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    completed: bool = False


class TaskResponse(TaskCreate):
    id: int
