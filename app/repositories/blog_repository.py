"""
Blog repository for blog-specific database operations
"""
from typing import Optional

from sqlalchemy import select, desc, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blog import BlogPost, Category, Tag
from app.repositories.base import BaseRepository
from app.utils.pagination import PaginatedResult, paginate_async


class BlogPostRepository(BaseRepository[BlogPost]):
    """Repository for BlogPost model"""

    def __init__(self, db: AsyncSession):
        super().__init__(BlogPost, db)

    async def get_by_slug(self, slug: str) -> Optional[BlogPost]:
        result = await self.db.execute(
            select(BlogPost).where(BlogPost.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_paginated(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        author_id: Optional[int] = None,
        **filters,
    ) -> PaginatedResult:
        sort_column = getattr(BlogPost, sort_by, BlogPost.id)
        order = desc(sort_column) if sort_order.upper() == "DESC" else asc(sort_column)
        stmt = select(BlogPost).order_by(order)

        if keyword:
            pattern = f"%{keyword}%"
            stmt = stmt.where(
                or_(BlogPost.title.ilike(pattern), BlogPost.excerpt.ilike(pattern))
            )
        if status:
            stmt = stmt.where(BlogPost.status == status)
        if author_id:
            stmt = stmt.where(BlogPost.author_id == author_id)

        return await paginate_async(self.db, stmt, page=page, limit=limit)


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category model"""

    def __init__(self, db: AsyncSession):
        super().__init__(Category, db)

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        result = await self.db.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalar_one_or_none()


class TagRepository(BaseRepository[Tag]):
    """Repository for Tag model"""

    def __init__(self, db: AsyncSession):
        super().__init__(Tag, db)

    async def get_by_slug(self, slug: str) -> Optional[Tag]:
        result = await self.db.execute(select(Tag).where(Tag.slug == slug))
        return result.scalar_one_or_none()

