import enum
from sqlalchemy import Column, Enum, String
from database import Base
from schemas.base_entity import BaseEntity
from sqlalchemy.orm import relationship

class Company_Mode(enum.Enum):
    Active = 1
    Inactive = 2
    
class Company_Rating(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Company(BaseEntity, Base):
    __tablename__ = "companies"
    
    name = Column(String) 
    description = Column(String) 
    mode = Column(Enum(Company_Mode), default=Company_Mode.Active)
    rating = Column(Enum(Company_Rating), default=Company_Rating.MEDIUM)
    
    users = relationship("User", back_populates="company")
    