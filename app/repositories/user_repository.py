"""
User repository for user-specific database operations
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import User, Role, UserRole
from app.repositories.base import BaseRepository
from app.utils.pagination import PaginatedResult, paginate


class UserRepository(BaseRepository[User]):
    """Repository for User model"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            email: User email
            
        Returns:
            User or None if not found
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_paginated(
        self,
        page: int = 1,
        limit: Optional[int] = 10,
        sort_by: str = "created_at",
        sort_order: str = "DESC",
        keyword: Optional[str] = None,
        **filters
    ) -> PaginatedResult:
        """
        Get paginated users with search
        
        Args:
            page: Page number
            limit: Items per page
            sort_by: Field to sort by
            sort_order: Sort order (ASC or DESC)
            keyword: Search keyword
            **filters: Additional filters
            
        Returns:
            PaginatedResult object
        """
        query = self.db.query(User)
        
        # Apply keyword search
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter(
                or_(
                    User.name.like(search_pattern),
                    User.email.like(search_pattern)
                )
            )
        
        # Apply sorting
        from sqlalchemy import desc, asc
        sort_column = getattr(User, sort_by, User.id)
        if sort_order.upper() == "ASC":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        return paginate(query, page=page, limit=limit)


class RoleRepository(BaseRepository[Role]):
    """Repository for Role model"""
    
    def __init__(self, db: Session):
        super().__init__(Role, db)
    
    def get_by_name(self, name: str) -> Optional[Role]:
        """
        Get role by name
        
        Args:
            name: Role name
            
        Returns:
            Role or None if not found
        """
        return self.db.query(Role).filter(Role.name == name).first()


class UserRoleRepository(BaseRepository[UserRole]):
    """Repository for UserRole model"""
    
    def __init__(self, db: Session):
        super().__init__(UserRole, db)
    
    def get_user_roles(self, user_id: int) -> List[Role]:
        """
        Get all roles for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of roles
        """
        user_roles = self.db.query(UserRole).filter(UserRole.user_id == user_id).all()
        return [ur.role for ur in user_roles]
    
    def assign_role(self, user_id: int, role_id: int) -> UserRole:
        """
        Assign a role to a user
        
        Args:
            user_id: User ID
            role_id: Role ID
            
        Returns:
            UserRole object
        """
        user_role = UserRole(user_id=user_id, role_id=role_id)
        return self.create(user_role)
    
    def remove_role(self, user_id: int, role_id: int) -> bool:
        """
        Remove a role from a user
        
        Args:
            user_id: User ID
            role_id: Role ID
            
        Returns:
            True if removed, False if not found
        """
        user_role = self.db.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        ).first()
        
        if user_role:
            self.db.delete(user_role)
            self.db.commit()
            return True
        return False
