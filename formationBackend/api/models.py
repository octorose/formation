from django.db import models

class Agent(models.Model):
    ROLE_CHOICES = [
        ('RH', 'RH'),
        ('ResponsableFormation', 'Responsable Formation'),
        ('ResponsableEcoleFormation', 'Responsable Ecole Formation'),
        ('Formateur', 'Formateur'),
        ('Superviseur', 'Superviseur'),
        ('Personnel', 'Personnel'),
    ]
    password = models.CharField(max_length=100 , null=True)
    email = models.EmailField(max_length=100, unique=True, null=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    addresse = models.CharField(max_length=255)
    cin = models.CharField(max_length=20, unique=True)
    numerotel = models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Personnel')
    username = models.CharField(max_length=100, unique=True , null=True)
    last_login = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    # Specify unique related_name and related_query_name for groups and user_permissions
    groups = models.ManyToManyField('auth.Group', related_name='agent_groups', related_query_name='agent_group')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='agent_user_permissions', related_query_name='agent_user_permission')

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
