from __future__ import annotations
from typing import Iterable, Optional
from sqlalchemy.orm import Session
from . import models, schemas


def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    task = models.Task(title=task_in.title, description=task_in.description or "", status=models.TaskStatus.created)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: str) -> Optional[models.Task]:
    return db.get(models.Task, task_id)


def list_tasks(db: Session, skip: int = 0, limit: int = 100) -> Iterable[models.Task]:
    return db.query(models.Task).offset(skip).limit(limit).all()


def update_task(db: Session, task: models.Task, updates: schemas.TaskUpdate) -> models.Task:
    data = updates.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()
