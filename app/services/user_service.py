"""
User service for user-related business logic
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repository import UserRepository, RoleRepository
from app.core.security import hash_password
from app.utils.pagination import PaginatedResult


class UserService:
    """Service for user-related business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User or None if not found
        """
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            email: User email
            
        Returns:
            User or None if not found
        """
        return self.user_repository.get_by_email(email)
    
    def get_users(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None
    ) -> PaginatedResult:
        """
        Get paginated users
        
        Args:
            page: Page number
            limit: Items per page
            sort_by: Field to sort by
            sort_order: Sort order (ASC or DESC)
            keyword: Search keyword
            
        Returns:
            PaginatedResult object
        """
        return self.user_repository.get_paginated(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            keyword=keyword
        )
    
    def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if email already exists
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password
        )
        
        return self.user_repository.create(user)
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """
        Update a user
        
        Args:
            user_id: User ID
            user_data: User update data
            
        Returns:
            Updated user
            
        Raises:
            HTTPException: If user not found or email already exists
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if email already exists (for different user)
        if user_data.email and user_data.email != user.email:
            existing_user = self.user_repository.get_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            user.email = user_data.email
        
        # Update fields
        if user_data.name is not None:
            user.name = user_data.name
        
        if user_data.password is not None:
            user.password = hash_password(user_data.password)
        
        return self.user_repository.update(user)
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted
            
        Raises:
            HTTPException: If user not found
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return self.user_repository.delete(user_id)
