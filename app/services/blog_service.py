"""
Blog service for blog-related business logic
"""
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.blog import BlogPost
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from app.repositories.blog_repository import BlogPostRepository
from app.utils.pagination import PaginatedResult


class BlogPostService:
    """Service for blog post-related business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.blog_post_repository = BlogPostRepository(db)
    
    def get_blog_post_by_id(self, post_id: int) -> Optional[BlogPost]:
        """
        Get blog post by ID
        
        Args:
            post_id: Blog post ID
            
        Returns:
            BlogPost or None if not found
        """
        return self.blog_post_repository.get_by_id(post_id)
    
    def get_blog_post_by_slug(self, slug: str) -> Optional[BlogPost]:
        """
        Get blog post by slug
        
        Args:
            slug: Blog post slug
            
        Returns:
            BlogPost or None if not found
        """
        return self.blog_post_repository.get_by_slug(slug)
    
    def get_blog_posts(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        author_id: Optional[int] = None
    ) -> PaginatedResult:
        """
        Get paginated blog posts
        
        Args:
            page: Page number
            limit: Items per page
            sort_by: Field to sort by
            sort_order: Sort order (ASC or DESC)
            keyword: Search keyword
            status: Filter by status
            author_id: Filter by author
            
        Returns:
            PaginatedResult object
        """
        return self.blog_post_repository.get_paginated(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            keyword=keyword,
            status=status,
            author_id=author_id
        )
    
    def create_blog_post(self, post_data: BlogPostCreate) -> BlogPost:
        """
        Create a new blog post
        
        Args:
            post_data: Blog post creation data
            
        Returns:
            Created blog post
            
        Raises:
            HTTPException: If slug already exists
        """
        # Check if slug already exists
        existing_post = self.blog_post_repository.get_by_slug(post_data.slug)
        if existing_post:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slug already exists"
            )
        
        # Create blog post
        post = BlogPost(**post_data.model_dump())
        
        return self.blog_post_repository.create(post)
    
    def update_blog_post(self, post_id: int, post_data: BlogPostUpdate) -> BlogPost:
        """
        Update a blog post
        
        Args:
            post_id: Blog post ID
            post_data: Blog post update data
            
        Returns:
            Updated blog post
            
        Raises:
            HTTPException: If post not found or slug already exists
        """
        post = self.blog_post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog post not found"
            )
        
        # Check if slug already exists (for different post)
        if post_data.slug and post_data.slug != post.slug:
            existing_post = self.blog_post_repository.get_by_slug(post_data.slug)
            if existing_post:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Slug already exists"
                )
        
        # Update fields
        for field, value in post_data.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        
        return self.blog_post_repository.update(post)
    
    def delete_blog_post(self, post_id: int) -> bool:
        """
        Delete a blog post
        
        Args:
            post_id: Blog post ID
            
        Returns:
            True if deleted
            
        Raises:
            HTTPException: If post not found
        """
        post = self.blog_post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog post not found"
            )
        
        return self.blog_post_repository.delete(post_id)
