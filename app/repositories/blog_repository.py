"""
Blog repository for blog-specific database operations
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.blog import BlogPost, Category, Tag
from app.repositories.base import BaseRepository
from app.utils.pagination import PaginatedResult, paginate


class BlogPostRepository(BaseRepository[BlogPost]):
    """Repository for BlogPost model"""
    
    def __init__(self, db: Session):
        super().__init__(BlogPost, db)
    
    def get_by_slug(self, slug: str) -> Optional[BlogPost]:
        """
        Get blog post by slug
        
        Args:
            slug: Blog post slug
            
        Returns:
            BlogPost or None if not found
        """
        return self.db.query(BlogPost).filter(BlogPost.slug == slug).first()
    
    def get_paginated(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        author_id: Optional[int] = None,
        **filters
    ) -> PaginatedResult:
        """
        Get paginated blog posts with filters
        
        Args:
            page: Page number
            limit: Items per page
            sort_by: Field to sort by
            sort_order: Sort order (ASC or DESC)
            keyword: Search keyword
            status: Filter by status
            author_id: Filter by author
            **filters: Additional filters
            
        Returns:
            PaginatedResult object
        """
        query = self.db.query(BlogPost)
        
        # Apply keyword search
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter(
                or_(
                    BlogPost.title.like(search_pattern),
                    BlogPost.excerpt.like(search_pattern)
                )
            )
        
        # Apply status filter
        if status:
            query = query.filter(BlogPost.status == status)
        
        # Apply author filter
        if author_id:
            query = query.filter(BlogPost.author_id == author_id)
        
        # Apply sorting
        from sqlalchemy import desc, asc
        sort_column = getattr(BlogPost, sort_by, BlogPost.id)
        if sort_order.upper() == "ASC":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        return paginate(query, page=page, limit=limit)


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category model"""
    
    def __init__(self, db: Session):
        super().__init__(Category, db)
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        """
        Get category by slug
        
        Args:
            slug: Category slug
            
        Returns:
            Category or None if not found
        """
        return self.db.query(Category).filter(Category.slug == slug).first()


class TagRepository(BaseRepository[Tag]):
    """Repository for Tag model"""
    
    def __init__(self, db: Session):
        super().__init__(Tag, db)
    
    def get_by_slug(self, slug: str) -> Optional[Tag]:
        """
        Get tag by slug
        
        Args:
            slug: Tag slug
            
        Returns:
            Tag or None if not found
        """
        return self.db.query(Tag).filter(Tag.slug == slug).first()
