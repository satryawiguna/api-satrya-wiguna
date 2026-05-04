"""
Blog service for blog-related business logic
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, DuplicateError
from app.models.blog import BlogPost
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from app.repositories.blog_repository import BlogPostRepository
from app.utils.pagination import PaginatedResult


class BlogPostService:
    """Service for blog post-related business logic"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.blog_post_repository = BlogPostRepository(db)

    async def get_blog_post_by_id(self, post_id: int) -> Optional[BlogPost]:
        return await self.blog_post_repository.get_by_id(post_id)

    async def get_blog_post_by_slug(self, slug: str) -> Optional[BlogPost]:
        return await self.blog_post_repository.get_by_slug(slug)

    async def get_blog_posts(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        author_id: Optional[int] = None,
    ) -> PaginatedResult:
        return await self.blog_post_repository.get_paginated(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            keyword=keyword,
            status=status,
            author_id=author_id,
        )

    async def create_blog_post(self, post_data: BlogPostCreate) -> BlogPost:
        existing_post = await self.blog_post_repository.get_by_slug(post_data.slug)
        if existing_post:
            raise DuplicateError("Slug already exists")
        post = BlogPost(**post_data.model_dump())
        return await self.blog_post_repository.create(post)

    async def update_blog_post(self, post_id: int, post_data: BlogPostUpdate) -> BlogPost:
        post = await self.blog_post_repository.get_by_id(post_id)
        if not post:
            raise NotFoundError("Blog post not found")

        if post_data.slug and post_data.slug != post.slug:
            existing_post = await self.blog_post_repository.get_by_slug(post_data.slug)
            if existing_post:
                raise DuplicateError("Slug already exists")

        for field, value in post_data.model_dump(exclude_unset=True).items():
            setattr(post, field, value)

        return await self.blog_post_repository.update(post)

    async def delete_blog_post(self, post_id: int) -> bool:
        post = await self.blog_post_repository.get_by_id(post_id)
        if not post:
            raise NotFoundError("Blog post not found")
        return await self.blog_post_repository.delete(post_id)
