from datetime import datetime, UTC
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models import company
from models.company import CompanyCreateModel, CompanySearchModel, CompanySearchResponseModel, CompanyUpdateModel, CompanyViewModel
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


def search_companies(db: Session, search_params: CompanySearchModel) -> CompanySearchResponseModel:
    query = db.query(Company).filter_by(**search_params.get_filter())
    
    count = query.count()
    companies = query.offset((search_params.page - 1) * search_params.page_size).limit(search_params.page_size).all()
    
    data = [CompanyViewModel.model_validate(c, from_attributes=True) for c in companies]
    
    return CompanySearchResponseModel(
        page=search_params.page,
        page_size=search_params.page_size,
        total=count,
        data=data
    )
