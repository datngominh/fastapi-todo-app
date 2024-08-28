from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from models.company import CompanySearchModel, CompanySearchResponseModel, CompanyUpdateModel, CompanyCreateModel, CompanyViewModel
from repositories import CompanyRepository
from services.exception import ResourceNotFoundError

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("/{company_id}", response_model=CompanyViewModel)
def get_company(company_id: str, db: Session = Depends(get_db_context)):
    company = CompanyRepository.get_company(db, company_id)
    if not company:
        raise ResourceNotFoundError(detail="Company not found")
    return company

@router.post("", response_model=CompanyViewModel, status_code=status.HTTP_201_CREATED)
def create_company(company: CompanyCreateModel, db: Session = Depends(get_db_context)):
    created_company = CompanyRepository.create_company(db, company)
    return created_company

@router.put("/{company_id}", response_model=CompanyViewModel)
def update_company(company_id: str, company: CompanyUpdateModel, db: Session = Depends(get_db_context)):
    updated_company = CompanyRepository.update_company(db, company_id, company)
    if not updated_company:
        raise ResourceNotFoundError(detail="Company not found")
    return updated_company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: str, db: Session = Depends(get_db_context)):
    deleted_company = CompanyRepository.delete_company(db, company_id)
    if not deleted_company:
        raise ResourceNotFoundError(detail="Company not found")
    return None

@router.post("/search", response_model=CompanySearchResponseModel)
def search_companies(search_params: CompanySearchModel, db: Session = Depends(get_db_context)):
    companies = CompanyRepository.search_companies(db, search_params)
    return companies