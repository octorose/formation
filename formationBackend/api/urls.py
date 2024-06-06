# mybackend/api/urls.py

from django.urls import path
from .views import CreateSupervisorView

urlpatterns = [
path('api/create_supervisor', CreateSupervisorView.as_view(), name='create_supervisor'), 
]
