
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field
from .models import TaskStatus


class TaskBase(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=10000)
    status: Optional[TaskStatus] = None


class TaskCreate(TaskBase):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default="", max_length=10000)


class TaskUpdate(TaskBase):
    pass


class TaskRead(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus

    model_config = {"from_attributes": True}
