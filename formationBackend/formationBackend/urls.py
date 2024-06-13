
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView 
from api.views import CreateSupervisorView, CreatePersonnelView, RegisterView, CustomTokenObtainPairView, CreateRHView, PersonnelListView, PersonnelCountByMonthAPIView, PersonnelSumByEtatView

urlpatterns = [
    path('api/create_supervisor/', CreateSupervisorView.as_view(), name='create_supervisor'),
    path('api/create_personnel/', CreatePersonnelView.as_view(), name='create_personnel'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/create_rh/', CreateRHView.as_view(), name='create_rh'),
    path('api/personnel/', PersonnelListView.as_view(), name='personnel-list'),
    path('api/personnel-count-by-month/', PersonnelCountByMonthAPIView.as_view(), name='personnel-count-by-month'),
    path('api/personnel-sum-by-etat/', PersonnelSumByEtatView.as_view(), name='personnel-sum-by-etat'),
]
