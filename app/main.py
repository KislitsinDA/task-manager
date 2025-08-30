
from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import Base, engine, get_db

app = FastAPI(title="Task Manager", version="1.0.0", description="Simple CRUD for tasks with FastAPI")

# Create tables on startup (SQLite)
Base.metadata.create_all(bind=engine)


@app.post("/tasks", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED, summary="Create a task")
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = crud.create_task(db, task_in)
    return task


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead, summary="Get task by ID")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.get("/tasks", response_model=List[schemas.TaskRead], summary="List tasks")
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return crud.list_tasks(db, skip=skip, limit=limit)


@app.patch("/tasks/{task_id}", response_model=schemas.TaskRead, summary="Update task (partial)")
def update_task(task_id: str, updates: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task = crud.update_task(db, task, updates)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete task")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    crud.delete_task(db, task)
    return None
