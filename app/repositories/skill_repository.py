"""
Skill repository for skill-specific database operations
"""
from typing import Optional

from sqlalchemy import select, desc, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.other import Skill
from app.repositories.base import BaseRepository
from app.utils.pagination import PaginatedResult, paginate_async


class SkillRepository(BaseRepository[Skill]):
    """Repository for Skill model"""

    def __init__(self, db: AsyncSession):
        super().__init__(Skill, db)

    async def get_paginated(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "sort_order",
        sort_order: str = "ASC",
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        **filters,
    ) -> PaginatedResult:
        sort_column = getattr(Skill, sort_by, Skill.sort_order)
        order = asc(sort_column) if sort_order.upper() == "ASC" else desc(sort_column)
        stmt = select(Skill).order_by(order)

        if keyword:
            pattern = f"%{keyword}%"
            stmt = stmt.where(
                or_(Skill.name.ilike(pattern), Skill.category.ilike(pattern))
            )
        if category:
            stmt = stmt.where(Skill.category == category)

        return await paginate_async(self.db, stmt, page=page, limit=limit)

