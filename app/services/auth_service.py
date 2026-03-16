"""
Authentication service
"""
from typing import Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import (
    verify_password, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.schemas.auth import UserWithRolesResponse, RoleResponse


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User if authenticated, None otherwise
        """
        user = self.user_repository.get_by_email(email)
        
        if not user:
            return None
        
        if not verify_password(password, user.password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def generate_token(self, user: User) -> str:
        """
        Generate access token for user
        
        Args:
            user: User object
            
        Returns:
            Access token string
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "type": "access"
        }
        
        return create_access_token(token_data)
    
    def get_user_with_roles(self, user: User) -> UserWithRolesResponse:
        """
        Get user data with roles
        
        Args:
            user: User object
            
        Returns:
            UserWithRolesResponse
        """
        roles = []
        for user_role in user.user_roles:
            roles.append(RoleResponse(
                id=user_role.role.id,
                name=user_role.role.name
            ))
        
        return UserWithRolesResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            isActive=user.is_active,
            roles=roles
        )
