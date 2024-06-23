from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Agent, Ligne, Personnel, Superviseur, Module, ResponsableEcoleFormation, Formateur

class CustomTokenObtainPairViewTests(APITestCase):

    def setUp(self):
        self.agent = Agent.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            role='Superviseur',
            password='password',
            prenom='Test',
            nom='User',
            date_naissance='1990-01-01',
            addresse='Test Address',
            cin='123456789',
            numerotel='1234567890'
        )

    def test_token_obtain_pair(self):
        print("Test: Login.")
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CreateSupervisorViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.agent = Agent.objects.create_user(
            username='admin',
            email='admin@example.com',
            role='Superviseur',
            password='adminpassword',
            prenom='Admin',
            nom='User',
            date_naissance='1980-01-01',
            addresse='Admin Address',
            cin='987654321',
            numerotel='0987654321'
        )
        self.ligne = Ligne.objects.create(name='Test Ligne')  # Creating the required Ligne object
        refresh = RefreshToken.for_user(self.agent)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_supervisor(self):
        print("Test: Create supervisor.")
        url = reverse('create_supervisor')
        data = {
            'agent': {
                'username': 'supervisor',
                'email': 'supervisor@example.com',
                'password': 'supervisorpassword',
                'prenom': 'Supervisor',
                'nom': 'User',
                'date_naissance': '1990-01-01',
                'addresse': 'Supervisor Address',
                'cin': '123456789',
                'numerotel': '1234567890'
            },
            'ligne_id': self.ligne.id  # Using the ID of the created Ligne
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_supervisor_without_ligne(self):
        print("Test: Attempt to create a supervisor without providing a ligne ID.")
        url = reverse('create_supervisor')
        data = {
            'agent': {
                'username': 'supervisor',
                'email': 'supervisor@example.com',
                'password': 'supervisorpassword',
                'prenom': 'Supervisor',
                'nom': 'User',
                'date_naissance': '1990-01-01',
                'addresse': 'Supervisor Address',
                'cin': '123456789',
                'numerotel': '1234567890'
            }
            # No 'ligne_id' provided intentionally
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_supervisor_without_token(self):
        print("Test: Attempt to create a supervisor without a token.")
        url = reverse('create_supervisor')
        data = {
            'agent': {
                'username': 'supervisor',
                'email': 'supervisor@example.com',
                'password': 'supervisorpassword',
                'prenom': 'Supervisor',
                'nom': 'User',
                'date_naissance': '1990-01-01',
                'addresse': 'Supervisor Address',
                'cin': '123456789',
                'numerotel': '1234567890'
            },
            'ligne_id': self.ligne.id  # Using the ID of the created Ligne
        }
        # Clearing credentials to simulate no token being provided
        self.client.credentials()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_supervisor_list(self):
        print("Test: List supervisors.")
        url = reverse('supervisor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supervisor_search(self):
        print("Test: Search supervisors.")
        url = reverse('supervisor-search')
        response = self.client.get(url, {'query': 'supervisor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supervisor_delete(self):
        print("Test: Delete supervisor.")
        supervisor = Superviseur.objects.create(agent=self.agent, ligne=self.ligne)
        url = reverse('delete_superviseur', kwargs={'pk': supervisor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CreatePersonnelViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.agent = Agent.objects.create_user(
            username='admin',
            email='admin@example.com',
            role='Superviseur',
            password='adminpassword',
            prenom='Admin',
            nom='User',
            date_naissance='1980-01-01',
            addresse='Admin Address',
            cin='987654321',
            numerotel='0987654321'
        )
        refresh = RefreshToken.for_user(self.agent)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_personnel(self):
        print("Test: Create personnel.")
        url = reverse('create_personnel')
        data = {
            'agent': {
                'username': 'personnel',
                'email': 'personnel@example.com',
                'password': 'personnelpassword',
                'prenom': 'Personnel',
                'nom': 'User',
                'date_naissance': '1990-01-01',
                'addresse': 'Personnel Address',
                'cin': '123456789',
                'numerotel': '1234567890'
            },
            'etat': 'Active'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_personnel_without_token(self):
        print("Test: Attempt to create personnel without a token.")
        url = reverse('create_personnel')
        data = {
            'agent': {
                'username': 'personnel',
                'email': 'personnel@example.com',
                'password': 'personnelpassword',
                'prenom': 'Personnel',
                'nom': 'User',
                'date_naissance': '1990-01-01',
                'addresse': 'Personnel Address',
                'cin': '123456789',
                'numerotel': '1234567890'
            },
            'etat': 'Active'
        }
        # Clearing credentials to simulate no token being provided
        self.client.credentials()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_personnel_list(self):
        print("Test: List personnel.")
        url = reverse('personnel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_personnel_sum_by_etat(self):
        print("Test: Sum personnel by etat.")
        url = reverse('personnel-sum-by-etat')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_personnel_update(self):
        print("Test: Update personnel.")
        personnel = Personnel.objects.create(agent=self.agent, etat='Active')
        url = reverse('update_personnel', kwargs={'pk': personnel.pk})
        data = {
            'agent': {
                'username': 'updated_personnel',
                'email': 'updated_personnel@example.com',
                'password': 'updatedpassword',
                'prenom': 'UpdatedPersonnel',
                'nom': 'User',
                'date_naissance': '1991-01-01',
                'addresse': 'Updated Personnel Address',
                'cin': '123456780',
                'numerotel': '1234567891'
            },
            'etat': 'Inactive'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ModuleViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.agent = Agent.objects.create_user(
            username='admin',
            email='admin@example.com',
            role='Superviseur',
            password='adminpassword',
            prenom='Admin',
            nom='User',
            date_naissance='1980-01-01',
            addresse='Admin Address',
            cin='987654321',
            numerotel='0987654321'
        )
        refresh = RefreshToken.for_user(self.agent)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_module_list(self):
        print("Test: List modules.")
        url = reverse('module-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_module_create(self):
        print("Test: Create module.")
        url = reverse('module-create')
        data = {
            'name': 'Test Module',
            'description': 'Test Module Description'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

