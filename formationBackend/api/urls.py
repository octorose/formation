# mybackend/api/urls.py

from django.urls import path
from .views import (
    CreateSupervisorView,
    CreateResponsableFormationEcoleView,
    UpdateResponsableEcoleFormationView,
    DeleteResponsableFormationEcoleView,
    ResponsableFormationEcoleSearchView,
    ResponsableFormationListView,
     CreateFormateurView,
    UpdateFormateurView,
    DeleteFormateurView,
    ListFormateurView,
    SearchFormateurView
)
urlpatterns = [

path('api/create_supervisor', CreateSupervisorView.as_view(), name='create_supervisor'), 

path('responsable_formation_ecole/', ResponsableFormationListView.as_view(), name='list-responsable-formation'),
path('create-responsable_formation_ecole/', CreateResponsableFormationEcoleView.as_view(), name='create-responsable-formation-ecole'),
path('update-responsable_formation_ecole/<int:pk>/', UpdateResponsableEcoleFormationView.as_view(), name='update-responsable-formation-ecole'),
path('delete-responsable_formation_ecole/<int:pk>/', DeleteResponsableFormationEcoleView.as_view(), name='delete-responsable-formation-ecole'),
path('search-responsable_formation_ecole/', ResponsableFormationEcoleSearchView.as_view(), name='search-responsable-formation-ecole'),

path('formateurs/', ListFormateurView.as_view(), name='formateur-list'),
path('create-formateurs/', CreateFormateurView.as_view(), name='formateur-create'),
path('update-formateurs/<int:pk>/', UpdateFormateurView.as_view(), name='formateur-edit'),
path('delete-formateurs/<int:pk>/', DeleteFormateurView.as_view(), name='formateur-delete'),
path('search-formateurs/', SearchFormateurView.as_view(), name='formateur-search'),
]
