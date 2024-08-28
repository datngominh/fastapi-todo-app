from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from models.task import TaskCreateModel, TaskUpdateModel, TaskViewModel
from schemas import User
from services.exception import ResourceNotFoundError
from repositories import TaskRepository
from services import auth as AuthService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[TaskViewModel])
def get_all_tasks(db: Session = Depends(get_db_context), user: User = Depends(AuthService.token_interceptor)):
    tasks = TaskRepository.get_user_tasks(db, user.id)
    return tasks

@router.get("/{task_id}", response_model=TaskViewModel)
def get_task(task_id: str, db: Session = Depends(get_db_context)):
    task = TaskRepository.get_task(db, task_id)
    if not task:
        raise ResourceNotFoundError("Task not found")
    return task

@router.post("/", response_model=TaskViewModel, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreateModel, db: Session = Depends(get_db_context), user: User = Depends(AuthService.token_interceptor)):
    created_task = TaskRepository.create_task(db, task, user.id)
    return created_task

@router.put("/{task_id}", response_model=TaskViewModel)
def update_task(task_id: str, task: TaskUpdateModel, db: Session = Depends(get_db_context), user: User = Depends(AuthService.token_interceptor)):
    updated_task = TaskRepository.update_task(db, task_id, task, user.id)
    if not updated_task:
        raise ResourceNotFoundError("Task not found")
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db_context), user: User = Depends(AuthService.token_interceptor)):
    deleted_task = TaskRepository.delete_task(db, task_id, user.id)
    if not deleted_task:
        raise ResourceNotFoundError("Task not found")