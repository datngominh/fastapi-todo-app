from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from models.user import UserCreateModel, UserUpdateModel, UserViewModel
from schemas import User
from services.exception import ResourceNotFoundError
from repositories import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserViewModel])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_context)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserViewModel)
def get_user(user_id: str, db: Session = Depends(get_db_context)):
    user = UserRepository.get_user(db, user_id)
    return user

@router.post("/", response_model=UserViewModel, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateModel, db: Session = Depends(get_db_context)):
    user = UserRepository.create_user(db, user)
    return user

@router.put("/{user_id}", response_model=UserViewModel)
def update_user(user_id: str, user: UserUpdateModel, db: Session = Depends(get_db_context)):
    user = UserRepository.update_user(db, user_id, user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db_context)):
    UserRepository.delete_user(db, user_id)
    return None