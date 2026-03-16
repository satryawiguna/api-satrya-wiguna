"""
Project repository for project-specific database operations
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.project import Project
from app.repositories.base import BaseRepository
from app.utils.pagination import PaginatedResult, paginate


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model"""
    
    def __init__(self, db: Session):
        super().__init__(Project, db)
    
    def get_by_slug(self, slug: str) -> Optional[Project]:
        """
        Get project by slug
        
        Args:
            slug: Project slug
            
        Returns:
            Project or None if not found
        """
        return self.db.query(Project).filter(Project.slug == slug).first()
    
    def get_paginated(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None,
        featured: Optional[bool] = None,
        **filters
    ) -> PaginatedResult:
        """
        Get paginated projects with filters
        
        Args:
            page: Page number
            limit: Items per page
            sort_by: Field to sort by
            sort_order: Sort order (ASC or DESC)
            keyword: Search keyword
            featured: Filter by featured status
            **filters: Additional filters
            
        Returns:
            PaginatedResult object
        """
        query = self.db.query(Project)
        
        # Apply keyword search
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter(
                or_(
                    Project.title.like(search_pattern),
                    Project.description.like(search_pattern)
                )
            )
        
        # Apply featured filter
        if featured is not None:
            query = query.filter(Project.featured == featured)
        
        # Apply sorting
        from sqlalchemy import desc, asc
        sort_column = getattr(Project, sort_by, Project.id)
        if sort_order.upper() == "ASC":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        return paginate(query, page=page, limit=limit)
