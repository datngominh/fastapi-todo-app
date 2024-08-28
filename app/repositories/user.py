from datetime import datetime, UTC
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.company import CompanyCreateModel, CompanyUpdateModel, CompanyViewModel
from schemas.company import Company_Mode
from services import utils
from schemas import Company
from services.exception import InternalServerError, ResourceNotFoundError