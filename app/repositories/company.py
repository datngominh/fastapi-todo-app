from datetime import datetime, UTC
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.company import CompanyCreateModel, CompanyUpdateModel, CompanyViewModel
from schemas.company import Company_Mode
from services import utils
from schemas import Company
from services.exception import InternalServerError, ResourceNotFoundError

def create_company(db: Session, company: CompanyCreateModel) -> Company:
    new_company = Company(**company.model_dump())
    new_company.created_at = datetime.now(UTC)
    new_company.updated_at = new_company.created_at
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def get_company(db: Session, company_id: UUID) -> Company:
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise ResourceNotFoundError()
    return company


def update_company(db: Session, company_id: UUID, company: CompanyUpdateModel) -> Company:
    existing_company = get_company(db, company_id)
    for field, value in company.model_dump(exclude_unset=True).items():
        setattr(existing_company, field, value)
    existing_company.updated_at = datetime.now(UTC)
    db.commit()
    db.refresh(existing_company)
    return existing_company


def delete_company(db: Session, company_id: UUID) -> Company:
    existing_company = get_company(db, company_id)
    
    existing_company.updated_at = datetime.now(UTC)
    existing_company.mode = Company_Mode.Inactive
    
    db.commit()
    db.refresh(existing_company)
    return existing_company
