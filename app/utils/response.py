"""
Standardized API response wrapper
"""
from datetime import datetime
from typing import Any, Optional, Dict
from pydantic import BaseModel


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    total: int
    page: int
    limit: int
    totalPages: int
    hasNextPage: bool
    hasPreviousPage: bool


class APIResponse:
    """Standardized API response wrapper"""
    
    @staticmethod
    def success(
        message: str = "Success",
        status: int = 200,
        data: Optional[Any] = None,
        pagination: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create success response
        
        Args:
            message: Response message
            status: HTTP status code
            data: Response data
            pagination: Pagination metadata
            
        Returns:
            Standardized response dictionary
        """
        response = {
            "success": True,
            "status": status,
            "message": message,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        }
        
        if data is not None:
            response["data"] = data
        
        if pagination is not None:
            response["pagination"] = pagination
        
        return response
    
    @staticmethod
    def error(
        message: str = "Error",
        status: int = 400,
        errors: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Create error response
        
        Args:
            message: Error message
            status: HTTP status code
            errors: Error details
            
        Returns:
            Standardized error response dictionary
        """
        response = {
            "success": False,
            "status": status,
            "message": message,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        }
        
        if errors is not None:
            response["errors"] = errors
        
        return response


def create_pagination_meta(
    total: int,
    page: int,
    limit: int
) -> Dict[str, Any]:
    """
    Create pagination metadata
    
    Args:
        total: Total number of items
        page: Current page number
        limit: Items per page
        
    Returns:
        Pagination metadata dictionary
    """
    total_pages = (total + limit - 1) // limit if limit > 0 else 0
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "totalPages": total_pages,
        "hasNextPage": page < total_pages,
        "hasPreviousPage": page > 1
    }
