"""
Project service for project-related business logic
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, DuplicateError
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.project_repository import ProjectRepository
from app.utils.pagination import PaginatedResult


class ProjectService:
    """Service for project-related business logic"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.project_repository = ProjectRepository(db)

    async def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return await self.project_repository.get_by_id(project_id)

    async def get_project_by_slug(self, slug: str) -> Optional[Project]:
        return await self.project_repository.get_by_slug(slug)

    async def get_projects(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None,
        featured: Optional[bool] = None,
    ) -> PaginatedResult:
        return await self.project_repository.get_paginated(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            keyword=keyword,
            featured=featured,
        )

    async def create_project(self, project_data: ProjectCreate) -> Project:
        existing_project = await self.project_repository.get_by_slug(project_data.slug)
        if existing_project:
            raise DuplicateError("Slug already exists")
        project = Project(**project_data.model_dump())
        return await self.project_repository.create(project)

    async def update_project(self, project_id: int, project_data: ProjectUpdate) -> Project:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")

        if project_data.slug and project_data.slug != project.slug:
            existing_project = await self.project_repository.get_by_slug(project_data.slug)
            if existing_project:
                raise DuplicateError("Slug already exists")

        for field, value in project_data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)

        return await self.project_repository.update(project)

    async def delete_project(self, project_id: int) -> bool:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        return await self.project_repository.delete(project_id)
