from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Agent, Ligne

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


class CreateRHViewTests(APITestCase):

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

    def test_create_rh(self):
        print("Test: Create RH.")
        url = reverse('create_rh')
        data = {
            'agent': {
                'username': 'rhuser',
                'email': 'rhuser@example.com',
                'password': 'rhuserpassword',
                'prenom': 'RH',
                'nom': 'User',
                'date_naissance': '1990-01-01',
                'addresse': 'RH Address',
                'cin': '123456789',
                'numerotel': '1234567890'
            },
            'department': 'HR Department'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rh_without_token(self):
        print("Test: Attempt to create RH without a token.")
        url = reverse('create_rh')
        data = {
            'agent': {
                'username': 'rhuser',
                'email': 'rhuser@example.com',
                'password': 'rhuserpassword',
                'prenom': 'RH',
                'nom': 'User',
                'date_naissance': '1990-01-01',
                'addresse': 'RH Address',
                'cin': '123456789',
                'numerotel': '1234567890'
            },
            'department': 'HR Department'
        }
        # Clearing credentials to simulate no token being provided
        self.client.credentials()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PersonnelCountByMonthAPIViewTests(APITestCase):

    def setUp(self):
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
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.agent)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_personnel_count_by_month(self):
        url = reverse('personnel-count-by-month')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Agent, Formateur, Ligne, Poste, ResponsableEcoleFormation, Superviseur, Test, Personnel
from .serializers import FormateurSerializer, AgentSerializer
from django.contrib.auth.models import User


class FormateurAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Agent.objects.create_user(
            email='test@example.com',
            role='Formateur',
            password='password',
            prenom='Test',
            nom='User',
            date_naissance='1990-01-01',
            addresse='Test Address',
            cin='12345678',
            numerotel='1234567890',
            username='testuser'
        )
        self.formateur = Formateur.objects.create(agent=self.user)
        self.list_url = reverse('list-formateur')
        self.create_url = reverse('create-formateur')
        self.delete_url = reverse('delete-formateur', kwargs={'pk': self.formateur.id})
        self.update_url = reverse('update-formateur', kwargs={'pk': self.formateur.id})
        self.search_url = reverse('search-formateur')

    def test_list_formateur(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_formateur(self):
        data = {
            'agent': {
                'email': 'new@example.com',
                'role': 'Formateur',
                'prenom': 'New',
                'nom': 'User',
                'date_naissance': '1990-01-01',
                'addresse': 'New Address',
                'cin': '87654321',
                'numerotel': '0987654321',
                'username': 'newuser'
            },
            'isAffecteur': True,
            'Type': 'Practical'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('formateur_id', response.data)

    def test_search_formateur(self):
        response = self.client.get(self.search_url, {'query': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_update_formateur(self):
        data = {
            'agent': {
                'prenom': 'Updated'
            },
            'isAffecteur': False,
            'Type': 'Theorique'
        }
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['formateur']['agent']['prenom'], 'Updated')

    def test_delete_formateur(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AgentModelTest(APITestCase):
    def test_create_agent(self):
        agent = Agent.objects.create_user(
            email='test@example.com',
            role='Formateur',
            password='password',
            prenom='Test',
            nom='User',
            date_naissance='1990-01-01',
            addresse='Test Address',
            cin='12345678',
            numerotel='1234567890',
            username='testuser'
        )
        self.assertEqual(agent.email, 'test@example.com')
        self.assertTrue(agent.check_password('password'))




if __name__ == '__main__':
    import unittest
    unittest.main()

