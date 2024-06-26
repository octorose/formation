# middleware.py
from django.http import HttpResponseForbidden
from django.urls import reverse
import logging
from django.middleware.common import MiddlewareMixin

# class AuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if the user is authenticated
#         if not request.user.is_authenticated and request.path != reverse('token_obtain_pair'):
#             return HttpResponseForbidden("Authentication required.")
        
#         response = self.get_response(request)
#         return response
# # middleware.py

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        logger.info(f"Request: {request.method} {request.path}")
        
        response = self.get_response(request)
        
        # Log the response status
        logger.info(f"Response status: {response.status_code}")
        
        return response
# middleware.py

class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"  # Replace with your domain or '*' for all
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE, PUT"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
