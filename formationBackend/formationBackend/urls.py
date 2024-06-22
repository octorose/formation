
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView 
from api.views import CreateSupervisorView, CreatePersonnelView, RegisterView, CustomTokenObtainPairView , CreateContratView, EditContratView


urlpatterns = [
    path('api/create_supervisor/', CreateSupervisorView.as_view(), name='create_supervisor'),
    path('api/create_personnel/', CreatePersonnelView.as_view(), name='create_personnel'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    
    
    path('api/contrat/', CreateContratView.as_view(), name='create_contrat'),
    path('api/contrat/<int:pk>/', EditContratView.as_view(), name='edit_contrat'),
    
    
]
