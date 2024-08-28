from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from schemas.task import Task_Status, Task_Priority

class TaskBaseModel(BaseModel):
    id: UUID
    sumary: str
    description: Optional[str] = None
    status: Optional[Task_Status] = Task_Status.TODO
    priority: Optional[Task_Priority] = Task_Priority.MEDIUM
    user_id: UUID
       
    class Config:
        from_attributes = True
        
class TaskViewModel(TaskBaseModel):
    created_at: datetime | None = None
    update_at: datetime | None = None
        
class TaskCreateModel(BaseModel):
    sumary: str
    description: Optional[str] = None
    status: Optional[Task_Status] = Task_Status.TODO
    priority: Optional[Task_Priority] = Task_Priority.MEDIUM
    
class TaskUpdateModel(BaseModel):
    sumary: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Task_Status]= None
    priority: Optional[Task_Priority] = None
    