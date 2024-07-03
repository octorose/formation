# middleware.py
from django.http import HttpResponseForbidden
from django.urls import reverse
import logging
from django.middleware.common import MiddlewareMixin


logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request: {request.method} {request.path}")
        
        response = self.get_response(request)
        
        logger.info(f"Response status: {response.status_code}")
        
        return response


class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*" 
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE, PUT"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
