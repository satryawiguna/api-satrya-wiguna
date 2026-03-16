"""
Pagination utilities
"""
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Query


T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination query parameters"""
    page: int = 1
    limit: Optional[int] = 10
    sortBy: str = "id"
    sortOrder: str = "DESC"
    keyword: Optional[str] = None
    
    class Config:
        frozen = True


class PaginatedResult(Generic[T]):
    """Paginated query result"""
    
    def __init__(self, items: List[T], total: int, page: int, limit: int):
        self.items = items
        self.total = total
        self.page = page
        self.limit = limit
    
    @property
    def total_pages(self) -> int:
        """Calculate total pages"""
        if self.limit == 0:
            return 0
        return (self.total + self.limit - 1) // self.limit
    
    @property
    def has_next(self) -> bool:
        """Check if there's a next page"""
        return self.page < self.total_pages
    
    @property
    def has_previous(self) -> bool:
        """Check if there's a previous page"""
        return self.page > 1


def paginate(
    query: Query,
    page: int = 1,
    limit: Optional[int] = 10
) -> PaginatedResult:
    """
    Paginate a SQLAlchemy query
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        limit: Items per page (None for all items)
        
    Returns:
        PaginatedResult object
    """
    # Get total count
    total = query.count()
    
    # If no limit, return all items
    if limit is None:
        items = query.all()
        return PaginatedResult(items=items, total=total, page=1, limit=total)
    
    # Calculate offset
    offset = (page - 1) * limit
    
    # Get paginated items
    items = query.offset(offset).limit(limit).all()
    
    return PaginatedResult(items=items, total=total, page=page, limit=limit)
