# mybackend/api/urls.py
from django.urls import path
from .views import (
    CreateSupervisorView,
    CreateTestView,
    UpdateTestView,
    DeleteTestView,
    ListTestView,
    SearchTestView,
    CreateContratView,
    UpdateContratView,
    DeleteContratView,
    ListContratView,
    SearchContratView
)

urlpatterns = [
    path('api/create_supervisor/', CreateSupervisorView.as_view(), name='create_supervisor'),

    path('api/tests/', ListTestView.as_view(), name='test-list'),
    path('api/tests/create/', CreateTestView.as_view(), name='test-create'),
    path('api/tests/update/<int:pk>/', UpdateTestView.as_view(), name='test-edit'),
    path('api/tests/delete/<int:pk>/', DeleteTestView.as_view(), name='test-delete'),
    path('api/tests/search/', SearchTestView.as_view(), name='test-search'),

    path('api/contrats/', ListContratView.as_view(), name='contrat-list'),
    path('api/contrats/create/', CreateContratView.as_view(), name='contrat-create'),
    path('api/contrats/update/<int:pk>/', UpdateContratView.as_view(), name='contrat-edit'),
    path('api/contrats/delete/<int:pk>/', DeleteContratView.as_view(), name='contrat-delete'),
    path('api/contrats/search/', SearchContratView.as_view(), name='contrat-search'),
]
