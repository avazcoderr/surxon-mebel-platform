from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from rest_framework.exceptions import (
    NotFound, ValidationError as DRFValidationError,
    PermissionDenied, AuthenticationFailed, MethodNotAllowed
)
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides unified error responses
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Define the custom response format
    custom_response_data = {
        "success": False,
        "message": "An error occurred",
        "errors": None
    }
    
    if response is not None:
        # Handle DRF exceptions
        if isinstance(exc, DRFValidationError):
            custom_response_data["message"] = "Validation error"
            custom_response_data["errors"] = response.data
        elif isinstance(exc, NotFound):
            custom_response_data["message"] = "Resource not found"
            custom_response_data["errors"] = {"detail": str(exc)}
        elif isinstance(exc, PermissionDenied):
            custom_response_data["message"] = "Permission denied"
            custom_response_data["errors"] = {"detail": str(exc)}
        elif isinstance(exc, AuthenticationFailed):
            custom_response_data["message"] = "Authentication failed"
            custom_response_data["errors"] = {"detail": str(exc)}
        elif isinstance(exc, MethodNotAllowed):
            custom_response_data["message"] = "Method not allowed"
            custom_response_data["errors"] = {"detail": str(exc)}
        else:
            custom_response_data["message"] = "An error occurred"
            custom_response_data["errors"] = response.data
        
        # Log the error
        logger.error(f"API Error: {exc}", exc_info=True, extra={'context': context})
        
        return Response(custom_response_data, status=response.status_code)
    
    # Handle Django exceptions not caught by DRF
    if isinstance(exc, ValidationError):
        custom_response_data["message"] = "Validation error"
        custom_response_data["errors"] = exc.message_dict if hasattr(exc, 'message_dict') else {"detail": str(exc)}
        logger.error(f"Django Validation Error: {exc}", exc_info=True, extra={'context': context})
        return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, IntegrityError):
        custom_response_data["message"] = "Data integrity error"
        custom_response_data["errors"] = {"detail": "A database constraint was violated"}
        logger.error(f"Database Integrity Error: {exc}", exc_info=True, extra={'context': context})
        return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, Http404):
        custom_response_data["message"] = "Resource not found"
        custom_response_data["errors"] = {"detail": "The requested resource was not found"}
        logger.error(f"404 Error: {exc}", exc_info=True, extra={'context': context})
        return Response(custom_response_data, status=status.HTTP_404_NOT_FOUND)
    
    # Log unexpected errors
    logger.error(f"Unexpected Error: {exc}", exc_info=True, extra={'context': context})
    
    # Return None to use default DRF error handling for unhandled exceptions
    return None


class GlobalErrorHandlingMiddleware:
    """
    Middleware to catch any unhandled exceptions and return unified error responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """
        Handle exceptions that weren't caught by the view layer
        """
        # Only handle API requests (assuming they start with /api/)
        if not request.path.startswith('/api/'):
            return None
        
        logger.error(f"Unhandled Exception in API: {exception}", exc_info=True, extra={'request': request})
        
        error_response = {
            "success": False,
            "message": "Internal server error",
            "errors": {"detail": "An unexpected error occurred. Please try again later."}
        }
        
        return JsonResponse(error_response, status=500)