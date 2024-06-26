from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser

class AgentManager(BaseUserManager):
    def create_user(self, email, role, password=None, username=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if role != 'Personnel' and (not password or not username):
            raise ValueError('Password and username must be set for roles other than Personnel')

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)

        if role == 'Personnel':
            user.set_unusable_password()
        else:
            user.set_password(password)

        if username:
            user.username = username

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, role='Superviseur', password=password, username=username, **extra_fields)


class Agent(AbstractUser):
    ROLE_CHOICES = [
        ('RH', 'RH'),
        ('ResponsableFormation', 'Responsable Formation'),
        ('ResponsableEcoleFormation', 'Responsable Ecole Formation'),
        ('Formateur', 'Formateur'),
        ('Superviseur', 'Superviseur'),
        ('Personnel', 'Personnel'),
    ]

    # Define REQUIRED_FIELDS
    REQUIRED_FIELDS = ['email', 'prenom', 'nom', 'date_naissance', 'addresse', 'cin', 'numerotel', 'role']

    # Define your custom fields
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    addresse = models.CharField(max_length=255)
    cin = models.CharField(max_length=20, unique=True)
    numerotel = models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Personnel')

    # Add any additional fields as needed
    temporary_session = models.BooleanField(default=False)
     # Override username field to make it nullable
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"

class RH(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE,null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)

class ResponsableFormation(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE,null=True, blank=True)
    domain = models.CharField(max_length=100, blank=True, null=True)

class ResponsableEcoleFormation(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE,null=True, blank=True)
    school_name = models.CharField(max_length=100, blank=True, null=True)

class Formateur(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE,null=True, blank=True)
    isAffecteur = models.BooleanField(default=False)
    type=models.CharField(max_length=100)
class Ligne(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Superviseur(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, null=True, blank=True)
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE)

class Personnel(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE)
    etat = models.CharField(max_length=100, blank=True, null=True, default="Candidate")
class Poste(models.Model):
    name = models.CharField(max_length=100)
    lignes = models.ManyToManyField('Ligne', related_name='postes')
    
    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name