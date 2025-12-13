from rest_framework.response import Response
from rest_framework import status
from typing import Any, Optional, Dict


class APIResponse:
    """
    Utility class for creating unified API responses
    """
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK) -> Response:
        """
        Create a successful response
        
        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code
        
        Returns:
            Response object with unified format
        """
        response_data = {
            "success": True,
            "message": message,
            "data": data
        }
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(message: str = "Error occurred", errors: Optional[Dict] = None, status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
        """
        Create an error response
        
        Args:
            message: Error message
            errors: Detailed error information
            status_code: HTTP status code
        
        Returns:
            Response object with unified error format
        """
        response_data = {
            "success": False,
            "message": message,
            "errors": errors
        }
        return Response(response_data, status=status_code)
    
    @staticmethod
    def paginated_success(data: Any, count: int, next_url: Optional[str] = None, 
                         previous_url: Optional[str] = None, message: str = "Success") -> Response:
        """
        Create a paginated successful response
        
        Args:
            data: Response data
            count: Total count of items
            next_url: URL for next page
            previous_url: URL for previous page
            message: Success message
        
        Returns:
            Response object with unified paginated format
        """
        response_data = {
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "count": count,
                "next": next_url,
                "previous": previous_url
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)