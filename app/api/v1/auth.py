"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
    UserWithRolesResponse
)
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user
from app.models.user import User
from app.utils.response import APIResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])


# OpenAPI example for login response
LOGIN_EXAMPLE = {
    "example": {
        "success": True,
        "status": 200,
        "message": "Login successful",
        "data": {
            "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refreshToken": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6...",
            "tokenType": "Bearer",
            "expiresIn": "15m",
            "refreshExpiresIn": "7d",
            "user": {
                "id": 1,
                "name": "Admin User",
                "email": "admin@satryawiguna.me",
                "isActive": True,
                "roles": [
                    {
                        "id": 1,
                        "name": "Admin",
                        "slug": "admin"
                    }
                ]
            }
        },
        "timestamp": "2024-01-15T10:30:00Z"
    }
}


@router.post(
    "/login",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": LOGIN_EXAMPLE
            }
        }
    }
)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with email and password
    
    - **email**: User email address
    - **password**: User password
    
    Returns JWT access token
    """
    auth_service = AuthService(db)
    
    # Authenticate user
    user = auth_service.authenticate_user(request.email, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Generate token
    access_token = auth_service.generate_token(user)
    
    # Get user with roles
    user_with_roles = auth_service.get_user_with_roles(user)
    
    # Create response
    token_response = TokenResponse(
        accessToken=access_token,
        user=user_with_roles
    )
    
    return APIResponse.success(
        message="Login successful",
        data=token_response.model_dump()
    )


@router.post(
    "/refresh",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    - **refreshToken**: Valid refresh token
    
    Returns new JWT access token and refresh token
    """
    auth_service = AuthService(db)
    
    try:
        # Generate new tokens
        tokens = auth_service.refresh_access_token(request.refreshToken)
        
        # Get user for response
        token_obj = auth_service.refresh_token_repository.find_by_token(tokens["refresh_token"])
        user = auth_service.user_repository.get_by_id(token_obj.user_id)
        user_with_roles = auth_service.get_user_with_roles(user)
        
        # Create response
        token_response = TokenResponse(
            accessToken=tokens["access_token"],
            refreshToken=tokens["refresh_token"],
            user=user_with_roles
        )
        
        return APIResponse.success(
            message="Token refreshed successfully",
            data=token_response.model_dump()
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh token"
        )


@router.get(
    "/me",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user information
    
    Requires valid JWT access token in Authorization header:
    ```
    Authorization: Bearer <access_token>
    ```
    
    Returns user information with roles
    """
    auth_service = AuthService(db)
    
    # Get user with roles
    user_with_roles = auth_service.get_user_with_roles(current_user)
    
    return APIResponse.success(
        message="User retrieved successfully",
        data=user_with_roles.model_dump()
    )


@router.post(
    "/logout",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def logout(
    request: RefreshTokenRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout user by revoking refresh token
    
    - **refreshToken**: Refresh token to revoke
    
    Requires valid JWT access token in Authorization header
    """
    auth_service = AuthService(db)
    
    # Revoke refresh token
    success = auth_service.logout(request.refreshToken)
    
    if success:
        return APIResponse.success(
            message="Logout successful"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token"
        )


@router.post(
    "/forgot-password",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Request password reset
    
    - **email**: User email address
    
    Sends password reset link to user's email (not implemented yet)
    """
    # TODO: Implement password reset email sending
    return APIResponse.success(
        message="Password reset email sent (not implemented)"
    )


@router.post(
    "/reset-password",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset password with token
    
    - **token**: Password reset token from email
    - **password**: New password
    - **passwordConfirmation**: Password confirmation
    
    Resets user password (not implemented yet)
    """
    # TODO: Implement password reset logic
    if request.password != request.passwordConfirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    return APIResponse.success(
        message="Password reset successful (not implemented)"
    )


@router.post(
    "/change-password",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    
    - **currentPassword**: Current password
    - **newPassword**: New password
    - **newPasswordConfirmation**: New password confirmation
    
    Requires valid JWT access token in Authorization header
    """
    from app.core.security import verify_password, hash_password
    
    # Validate passwords match
    if request.newPassword != request.newPasswordConfirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match"
        )
    
    # Verify current password
    if not verify_password(request.currentPassword, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password = hash_password(request.newPassword)
    db.commit()
    
    return APIResponse.success(
        message="Password changed successfully"
    )
