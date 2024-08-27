import enum
from sqlalchemy import Column, ForeignKey, String, Uuid, Enum
from database import Base
from schemas.base_entity import BaseEntity
from sqlalchemy.orm import relationship

class Task_Priority(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    
class Task_Status(enum.Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3
    
class Task(BaseEntity, Base):
    __tablename__ = "tasks"
    
    sumary = Column(String) 
    description = Column(String) 
    status =  Column(Enum(Task_Status), default=Task_Status.TODO)
    priority = Column(Enum(Task_Priority), default=Task_Priority.MEDIUM)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)

    user = relationship("User")
    