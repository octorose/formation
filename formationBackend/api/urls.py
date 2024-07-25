# mybackend/api/urls.py
from django.urls import path
from .views import (
    CreateTestView,
    UpdateTestView,
    DeleteTestView,
    ListTestView,
    SearchTestView,
    CreateContratView,
    UpdateContratView,
    DeleteContratView,
    ListContratView,
    SearchContratView,
    CreateResponsableFormationEcoleView,
    UpdateResponsableEcoleFormationView,
    DeleteResponsableFormationEcoleView,
    ResponsableFormationEcoleSearchView,
    ResponsableFormationListView,
     CreateFormateurView,
    UpdateFormateurView,
    DeleteFormateurView,
    ListFormateurView,
    SearchFormateurView, UpdatePosteView, PosteListView, PosteSearchView, PosteDeleteView,PosteCreateView
)


urlpatterns = [
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


    path('create-postes/', PosteCreateView.as_view(), name='create_poste'),
    path('update-postes/<int:pk>/', UpdatePosteView.as_view(), name='update_poste'),
    path('postes/', PosteListView.as_view(), name='list_postes'),
    path('search-postes/', PosteSearchView.as_view(), name='search_postes'),
    path('delete-postes/<int:pk>/', PosteDeleteView.as_view(), name='delete_poste'),
]
