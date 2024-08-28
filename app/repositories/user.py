from datetime import datetime, UTC
from uuid import UUID
from sqlalchemy import false
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import User, get_password_hash
from services import utils
from schemas import Company
from services.exception import InternalServerError, ResourceNotFoundError
from models.user import UserCreateModel, UserUpdateModel, UserViewModel

def create_user(db: Session, user: UserCreateModel) -> UserViewModel:
    try:
        # Generate a unique UUID for the user
        user_id = str(UUID())

        # Create a new user instance
        new_user = User(
            id=user_id,
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        # Add the user to the database session
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Return the created user as a view model
        return UserViewModel.model_validate(new_user, from_attributes=True)

    except Exception as e:
        # Handle any exceptions and raise an internal server error
        raise InternalServerError("Failed to create user") from e


def get_user(db: Session, user_id: str) -> UserViewModel:
    # Retrieve the user from the database by ID
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        # If the user is not found, raise a resource not found error
        raise ResourceNotFoundError("User not found")

    # Return the user as a view model
    return UserViewModel.model_validate(user, from_attributes=True)


def update_user(db: Session, user_id: str, user: UserUpdateModel) -> UserViewModel:
    # Retrieve the user from the database by ID
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        # If the user is not found, raise a resource not found error
        raise ResourceNotFoundError("User not found")

    # Update the user's properties
    db_user.email = user.email or db_user.email
    db_user.first_name = user.first_name or db_user.first_name
    db_user.last_name = user.last_name or db_user.last_name    
    db_user.updated_at = datetime.now(UTC)

    # Commit the changes to the database
    db.commit()
    db.refresh(db_user)

    # Return the updated user as a view model
    return UserViewModel.model_validate(db_user, from_attributes=True)


def delete_user(db: Session, user_id: str):
    # Retrieve the user from the database by ID
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        # If the user is not found, raise a resource not found error
        raise ResourceNotFoundError("User not found")
    
    db_user.updated_at = datetime.now(UTC)
    db_user.is_active = False

    # Disable the user
    db.commit()
    db.refresh(db_user)
