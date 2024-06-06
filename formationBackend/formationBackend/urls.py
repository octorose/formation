
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView 
from api.views import CreateSupervisorView, CreatePersonnelView, RegisterView,EditFormateurView, CustomTokenObtainPairView,EditResponsableFormationEcoleView,CreateResponsableFormationEcoleView,CreateFormateurView

urlpatterns = [
    path('api/create_supervisor/', CreateSupervisorView.as_view(), name='create_supervisor'),
    path('api/create_personnel/', CreatePersonnelView.as_view(), name='create_personnel'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/responsableEcoleformation/', CreateResponsableFormationEcoleView.as_view(), name='create_responsableEcoleformation'),
    path('api/responsableEcoleformation/<int:pk>/',EditResponsableFormationEcoleView.as_view(), name='edit_responsableEcoleformation'),
    path('api/formateur/',CreateFormateurView.as_view(),name='create_formateur'),
    path('api/formateur/<int:pk>/',EditFormateurView.as_view(),name='edit_formateur'),

]
