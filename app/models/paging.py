from typing import Any, List, Optional
from pydantic import BaseModel, model_validator


class BasePagingParams(BaseModel):
    page: int = 1
    page_size: int = 10
    
    def get_filter(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True, exclude={"page", "page_size"}) 
    

class BasePagingResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool
    next_page: Optional[int]
    prev_page: Optional[int]
    data: List
    
    class Config:
        validate_assignment = False
    
    @model_validator(mode="before")
    def calculate_paging(cls, values):
        page = values.get('page')
        page_size = values.get('page_size')
        total = values.get('total')
        
        total_pages = (total + page_size - 1) // page_size  # Calculate total pages
        has_next = page < total_pages
        has_prev = page > 1
        next_page = page + 1 if has_next else None
        prev_page = page - 1 if has_prev else None
        
        values.update({
            'total_pages': total_pages,
            'has_next': has_next,
            'has_prev': has_prev,
            'next_page': next_page,
            'prev_page': prev_page
        })
        return values
        