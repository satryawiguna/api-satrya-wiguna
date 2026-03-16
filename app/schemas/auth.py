"""
Authentication schemas
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class RoleResponse(BaseModel):
    """Role response schema"""
    id: int
    name: str
    
    class Config:
        from_attributes = True


class UserWithRolesResponse(BaseModel):
    """User response with roles"""
    id: int
    name: str
    email: str
    isActive: bool
    roles: List[RoleResponse]
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    accessToken: str
    tokenType: str = "Bearer"
    expiresIn: str = "15m"
    user: UserWithRolesResponse


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refreshToken: str


class ForgotPasswordRequest(BaseModel):
    """Forgot password request schema"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request schema"""
    token: str
    password: str
    passwordConfirmation: str


class ChangePasswordRequest(BaseModel):
    """Change password request schema"""
    currentPassword: str
    newPassword: str
    newPasswordConfirmation: str
