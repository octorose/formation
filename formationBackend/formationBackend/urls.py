
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView 
from api.serializers import create_supervisor

urlpatterns = [
    path("api",include("djoser.urls")),
    path("api",include("djoser.urls.jwt")),
    path('api/', include('api.urls')),
    path('supervisor/create', create_supervisor, name='create_supervisor'),

]
