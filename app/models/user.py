from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserCreateModel(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str

class UserUpdateModel(BaseModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True

class UserViewModel(UserBaseModel):
    is_admin: bool
    created_at: datetime | None = None
    update_at: datetime | None = None
