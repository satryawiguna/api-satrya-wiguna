"""
Project repository for project-specific database operations
"""
from typing import Optional

from sqlalchemy import select, desc, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.repositories.base import BaseRepository
from app.utils.pagination import PaginatedResult, paginate_async


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model"""

    def __init__(self, db: AsyncSession):
        super().__init__(Project, db)

    async def get_by_slug(self, slug: str) -> Optional[Project]:
        result = await self.db.execute(
            select(Project).where(Project.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_paginated(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None,
        featured: Optional[bool] = None,
        **filters,
    ) -> PaginatedResult:
        sort_column = getattr(Project, sort_by, Project.id)
        order = desc(sort_column) if sort_order.upper() == "DESC" else asc(sort_column)
        stmt = select(Project).order_by(order)

        if keyword:
            pattern = f"%{keyword}%"
            stmt = stmt.where(
                or_(Project.title.ilike(pattern), Project.description.ilike(pattern))
            )
        if featured is not None:
            stmt = stmt.where(Project.featured == featured)

        return await paginate_async(self.db, stmt, page=page, limit=limit)

