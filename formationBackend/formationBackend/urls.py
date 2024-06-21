
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView 
from api.views import CreateSupervisorView,UpdatePersonnelView,PersonnelSearchView, ModuleCreateView, CreatePersonnelView, RegisterView, CustomTokenObtainPairView, CreateRHView, PersonnelListView, PersonnelCountByMonthAPIView, PersonnelSumByEtatView, DeletePersonnelView, ModuleListView, SupervisorListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/create_supervisor/', CreateSupervisorView.as_view(), name='create_supervisor'),
    path('api/supervisors/', SupervisorListView.as_view(), name='supervisor-list'),
    path('api/create_personnel/', CreatePersonnelView.as_view(), name='create_personnel'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/create_rh/', CreateRHView.as_view(), name='create_rh'),
    path('api/personnel/', PersonnelListView.as_view(), name='personnel-list'),
    path('api/personnel-count-by-month/', PersonnelCountByMonthAPIView.as_view(), name='personnel-count-by-month'),
    path('api/personnel-sum-by-etat/', PersonnelSumByEtatView.as_view(), name='personnel-sum-by-etat'),
    path('api/delete_personnel/<int:pk>/', DeletePersonnelView.as_view(), name='delete_personnel'),
    path('api/personnel-search/', PersonnelSearchView.as_view(), name='personnel-search'),
    path('api/update_personnel/<int:pk>/', UpdatePersonnelView.as_view(), name='update_personnel'),
    path('api/modules/', ModuleListView.as_view(), name='module-list'),
    path('api/modules/create/', ModuleCreateView.as_view(), name='module-create'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)