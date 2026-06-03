"""
Custom middleware for request validation and security.
"""

import json
import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestValidationMiddleware(MiddlewareMixin):
    """
    Validates incoming requests for common security issues.
    """
    
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10MB
    
    def process_request(self, request):
        """
        Validate request before processing.
        """
        
        # Check Content-Length header for large requests
        content_length = request.META.get('CONTENT_LENGTH', '')
        
        if content_length:
            try:
                if int(content_length) > self.MAX_BODY_SIZE:
                    logger.warning(f"Request exceeds size limit: {content_length} bytes")
                    return JsonResponse(
                        {"error": "Request body too large"},
                        status=413
                    )
            except (ValueError, TypeError):
                pass
        
        # Log request info for debugging
        logger.debug(f"{request.method} {request.path}")
        
        return None


class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Catches unexpected errors and returns clean JSON responses.
    """
    
    def process_exception(self, request, exception):
        """
        Handle exceptions and return JSON error response.
        """
        logger.exception(f"Unhandled exception: {exception}")
        
        return JsonResponse(
            {"error": "Internal server error"},
            status=500
        )
