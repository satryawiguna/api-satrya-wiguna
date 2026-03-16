"""
Project service for project-related business logic
"""
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.project_repository import ProjectRepository
from app.utils.pagination import PaginatedResult


class ProjectService:
    """Service for project-related business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.project_repository = ProjectRepository(db)
    
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """
        Get project by ID
        
        Args:
            project_id: Project ID
            
        Returns:
            Project or None if not found
        """
        return self.project_repository.get_by_id(project_id)
    
    def get_project_by_slug(self, slug: str) -> Optional[Project]:
        """
        Get project by slug
        
        Args:
            slug: Project slug
            
        Returns:
            Project or None if not found
        """
        return self.project_repository.get_by_slug(slug)
    
    def get_projects(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None,
        featured: Optional[bool] = None
    ) -> PaginatedResult:
        """
        Get paginated projects
        
        Args:
            page: Page number
            limit: Items per page
            sort_by: Field to sort by
            sort_order: Sort order (ASC or DESC)
            keyword: Search keyword
            featured: Filter by featured status
            
        Returns:
            PaginatedResult object
        """
        return self.project_repository.get_paginated(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            keyword=keyword,
            featured=featured
        )
    
    def create_project(self, project_data: ProjectCreate) -> Project:
        """
        Create a new project
        
        Args:
            project_data: Project creation data
            
        Returns:
            Created project
            
        Raises:
            HTTPException: If slug already exists
        """
        # Check if slug already exists
        existing_project = self.project_repository.get_by_slug(project_data.slug)
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slug already exists"
            )
        
        # Create project
        project = Project(**project_data.model_dump())
        
        return self.project_repository.create(project)
    
    def update_project(self, project_id: int, project_data: ProjectUpdate) -> Project:
        """
        Update a project
        
        Args:
            project_id: Project ID
            project_data: Project update data
            
        Returns:
            Updated project
            
        Raises:
            HTTPException: If project not found or slug already exists
        """
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Check if slug already exists (for different project)
        if project_data.slug and project_data.slug != project.slug:
            existing_project = self.project_repository.get_by_slug(project_data.slug)
            if existing_project:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Slug already exists"
                )
        
        # Update fields
        for field, value in project_data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        
        return self.project_repository.update(project)
    
    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project
        
        Args:
            project_id: Project ID
            
        Returns:
            True if deleted
            
        Raises:
            HTTPException: If project not found
        """
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        return self.project_repository.delete(project_id)
