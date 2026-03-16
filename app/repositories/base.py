"""
Base repository with common CRUD operations
"""
from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.core.database import Base
from app.utils.pagination import PaginatedResult, paginate


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository for common CRUD operations"""
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get entity by ID
        
        Args:
            id: Entity ID
            
        Returns:
            Entity or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: Optional[int] = 100,
        sort_by: str = "id",
        sort_order: str = "DESC"
    ) -> List[ModelType]:
        """
        Get all entities with optional pagination and sorting
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            sort_by: Field to sort by
            sort_order: Sort order (ASC or DESC)
            
        Returns:
            List of entities
        """
        query = self.db.query(self.model)
        
        # Apply sorting
        sort_column = getattr(self.model, sort_by, self.model.id)
        if sort_order.upper() == "ASC":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        if limit is None:
            return query.offset(skip).all()
        
        return query.offset(skip).limit(limit).all()
    
    def get_paginated(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "id",
        sort_order: str = "DESC",
        **filters
    ) -> PaginatedResult:
        """
        Get paginated entities
        
        Args:
            page: Page number
            limit: Items per page
            sort_by: Field to sort by
            sort_order: Sort order (ASC or DESC)
            **filters: Additional filter parameters
            
        Returns:
            PaginatedResult object
        """
        query = self.db.query(self.model)
        
        # Apply sorting
        sort_column = getattr(self.model, sort_by, self.model.id)
        if sort_order.upper() == "ASC":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        return paginate(query, page=page, limit=limit)
    
    def create(self, obj: ModelType) -> ModelType:
        """
        Create a new entity
        
        Args:
            obj: Entity to create
            
        Returns:
            Created entity
        """
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: ModelType) -> ModelType:
        """
        Update an existing entity
        
        Args:
            obj: Entity to update
            
        Returns:
            Updated entity
        """
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, id: int) -> bool:
        """
        Delete an entity by ID
        
        Args:
            id: Entity ID
            
        Returns:
            True if deleted, False if not found
        """
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        """
        Get total count of entities
        
        Returns:
            Total count
        """
        return self.db.query(self.model).count()
