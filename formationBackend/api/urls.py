# mybackend/api/urls.py

from django.urls import path
from .views import personnel_list
from .serializers import create_supervisor

urlpatterns = [
    path('personnel/', personnel_list, name='personnel_list'),
    path('supervisor/create', create_supervisor, name='create_supervisor'),
    # Add other URL patterns for your views
]
