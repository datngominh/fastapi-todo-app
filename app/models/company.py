from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from models.paging import BasePagingParams, BasePagingResponse
from schemas.company import Company_Mode, Company_Rating

class CompanyCreateModel(BaseModel):
    name : str
    description : Optional[str] = None
    mode : Company_Mode
    rating : Company_Rating
    
class CompanyUpdateModel(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    mode : Optional[Company_Mode] = None
    rating : Optional[Company_Rating] = None
    
class CompanySearchModel(BasePagingParams):
    id : Optional[UUID] = None
    name : Optional[str] = None
    description : Optional[str] = None
    mode : Optional[Company_Mode] = None
    rating : Optional[Company_Rating] = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
class CompanyViewModel(BaseModel):
    id : UUID
    name : str
    description : str
    mode : Company_Mode
    rating : Company_Rating
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True

    
class CompanySearchResponseModel(BasePagingResponse):
    data : list[CompanyViewModel] = []