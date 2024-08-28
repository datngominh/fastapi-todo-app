from datetime import datetime, UTC
from uuid import UUID
from sqlalchemy import false
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.task import Task
from services.exception import InternalServerError, ResourceNotFoundError
from models.task import TaskCreateModel, TaskUpdateModel, TaskViewModel
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import false
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from services.exception import InternalServerError, ResourceNotFoundError
from models.task import TaskCreateModel, TaskUpdateModel, TaskViewModel

def create_task(db: Session, task: TaskCreateModel, user_id: UUID) -> TaskViewModel:
    try:
        # Create a new task object
        new_task = Task(
            sumary=task.sumary,
            description=task.description,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            user_id = user_id
        )
        
        # Add the task to the database session
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        # Return the created task
        return TaskViewModel.model_validate(new_task, from_attributes=True)
    except Exception as e:
        # Handle any exceptions and raise an InternalServerError
        raise InternalServerError("Failed to create task") from e

def get_task(db: Session, task_id: UUID) -> TaskViewModel:
    try:
        # Retrieve the task from the database by its ID
        task = db.query(Task).filter(Task.id == task_id).first()
        
        # If the task doesn't exist, raise a ResourceNotFoundError
        if not task:
            raise ResourceNotFoundError("Task not found")
        
        # Return the task
        return TaskViewModel.model_validate(task, from_attributes=True)
    except Exception as e:
        # Handle any exceptions and raise an InternalServerError
        raise InternalServerError("Failed to get task") from e
    
def get_user_tasks(db: Session, user_id: UUID) -> TaskViewModel:
    try:
        # Retrieve the task from the database by its ID
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        
        # Return the task
        return  [TaskViewModel.model_validate(t, from_attributes=True) for t in tasks]
    except Exception as e:
        # Handle any exceptions and raise an InternalServerError
        raise InternalServerError("Failed to get task") from e

def update_task(db: Session, task_id: UUID, task: TaskUpdateModel, user_id: UUID) -> TaskViewModel:
    try:
        # Retrieve the task from the database by its ID
        db_task = db.query(Task).filter(Task.id == task_id and Task.user_id == user_id).first()
        
        # If the task doesn't exist, raise a ResourceNotFoundError
        if not db_task:
            raise ResourceNotFoundError("Task not found")
        
        # Update the task properties
        db_task.sumary = task.sumary or db_task.sumary
        db_task.description = task.description or db_task.description
        db_task.status = task.status or db_task.status
        db_task.priority = task.priority or db_task.priority
        db_task.updated_at = datetime.now(timezone.utc)
        
        # Commit the changes to the database
        db.commit()
        db.refresh(db_task)
        
        # Return the updated task
        return TaskViewModel.model_validate(db_task, from_attributes=True)
    except Exception as e:
        # Handle any exceptions and raise an InternalServerError
        raise InternalServerError("Failed to update task") from e

def delete_task(db: Session, task_id: UUID, user_id: UUID):
    try:
        # Retrieve the task from the database by its ID
        db_task = db.query(Task).filter(Task.id == task_id and Task.user_id == user_id).first()
        
        # If the task doesn't exist, raise a ResourceNotFoundError
        if not db_task:
            raise ResourceNotFoundError("Task not found")
        
        # Delete the task from the database
        db.delete(db_task)
        db.commit()
    except Exception as e:
        # Handle any exceptions and raise an InternalServerError
        raise InternalServerError("Failed to delete task") from e