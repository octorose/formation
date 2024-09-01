from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import (
    Agent, Group, RH, ResponsableFormation, ResponsableEcoleFormation, Ligne, Segment, 
    Formateur, Superviseur, Poste, Personnel, Polyvalence, Test, Contrat, Module, SegDepartement
)

class ModelsTestCase(TestCase):

    def setUp(self):
        self.email = 'octorose1337@gmail.com'
        # Create necessary instances for each test
        self.agent = Agent.objects.create_user(
            email=self.email,
            password='testpassword',
            role='Formateur',
            prenom='John',
            nom='Doe',
            date_naissance='1980-01-01',
            addresse='123 Test St',
            cin='123456789',
            numerotel='1234567890'
        )
        self.ligne = Ligne.objects.create(name='Ligne 1')
        self.group = Group.objects.create(name='Test Group', Effectif=10)
        self.segment = Segment.objects.create(agent=self.agent, ligne=self.ligne)
        self.formateur = Formateur.objects.create(
            agent=self.agent,
            isAffecteur=True,
            Type='Theorique',
            segment=self.segment
        )
        self.superviseur = Superviseur.objects.create(agent=self.agent)
        self.poste = Poste.objects.create(name='Poste 1')
        self.personnel = Personnel.objects.create(
            agent=self.agent,
            etat='Operateur',
            ligne=self.ligne,
            poste=self.poste,
            group=self.group
        )
        self.polyvalence = Polyvalence.objects.create(
            personnel=self.personnel,
            poste=self.poste,
            rating=8
        )

    def test_agent_creation(self):
        self.assertEqual(self.agent.email, self.email)
        self.assertTrue(self.agent.check_password('testpassword'))
        self.assertEqual(self.agent.role, 'Formateur')

    def test_agent_str(self):
        self.assertEqual(str(self.agent), 'John Doe (Formateur)')

    def test_group_creation(self):
        self.assertEqual(self.group.name, 'Test Group')
        self.assertEqual(self.group.Effectif, 10)

    def test_group_str(self):
        self.assertEqual(str(self.group), 'Test Group')

    def test_ligne_creation(self):
        self.assertEqual(self.ligne.name, 'Ligne 1')

    def test_ligne_str(self):
        self.assertEqual(str(self.ligne), 'Ligne 1')

    def test_segment_creation(self):
        self.assertEqual(self.segment.agent, self.agent)
        self.assertEqual(self.segment.ligne, self.ligne)

    def test_segment_str(self):
        self.assertEqual(str(self.segment), f'{self.segment.agent.prenom} {self.segment.agent.nom} (Segment)')

    def test_formateur_creation(self):
        self.assertEqual(self.formateur.agent, self.agent)
        self.assertEqual(self.formateur.Type, 'Theorique')
        self.assertEqual(self.formateur.segment, self.segment)

    def test_formateur_type_segment_consistency(self):
        self.formateur.Type = 'Pratique'
        self.formateur.segment = None
        with self.assertRaises(ValueError):
            self.formateur.save()

    def test_superviseur_creation(self):
        self.assertEqual(self.superviseur.agent, self.agent)
        self.assertIn(self.ligne, self.superviseur.lignes.all())

    def test_superviseur_str(self):
        self.assertEqual(str(self.superviseur), f'{self.agent.prenom} {self.agent.nom} (Superviseur)')

    def test_personnel_creation(self):
        self.assertEqual(self.personnel.agent, self.agent)
        self.assertEqual(self.personnel.etat, 'Operateur')
        self.assertEqual(self.personnel.ligne, self.ligne)
        self.assertEqual(self.personnel.poste, self.poste)
        self.assertEqual(self.personnel.group, self.group)

    def test_personnel_state_constraints(self):
        self.personnel.etat = 'Operateur'
        self.personnel.ligne = None
        self.personnel.poste = None
        with self.assertRaises(ValueError):
            self.personnel.save()

    def test_polyvalence_creation(self):
        self.assertEqual(self.polyvalence.personnel, self.personnel)
        self.assertEqual(self.polyvalence.poste, self.poste)
        self.assertEqual(self.polyvalence.rating, 8)

    def tearDown(self):
        # Delete the agent to avoid duplication issues
        self.agent.delete()
        # Delete other instances if necessary
        # Example: self.ligne.delete(), self.group.delete(), etc.
