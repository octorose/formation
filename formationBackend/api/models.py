from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser


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
        ('Segment', 'Segment'),  # Added Segment role
        ('Superviseur', 'Superviseur'),
        ('Personnel', 'Personnel'),
    ]

    REQUIRED_FIELDS = ['email', 'prenom', 'nom', 'date_naissance', 'addresse', 'cin', 'numerotel', 'role']

    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    addresse = models.CharField(max_length=255)
    cin = models.CharField(max_length=20, unique=True)
    numerotel = models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Personnel')

    temporary_session = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    site = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"
class RH(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)


class ResponsableFormation(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, null=True, blank=True)
    domain = models.CharField(max_length=100, blank=True, null=True)


class ResponsableEcoleFormation(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, null=True, blank=True)
class Ligne(models.Model):
    name = models.CharField(max_length=100)
    superviseur = models.ForeignKey('Superviseur', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Segment(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE, related_name='segments', null=True, blank=True)


class Formateur(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, null=True, blank=True)
    isAffecteur = models.BooleanField(default=False)
    Type = models.CharField(max_length=100, null=False, blank=False, default="Theorique")
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(Type='Pratique') & models.Q(segment__isnull=False)) |
                    (models.Q(Type__in=['Theorique', 'Other']) & models.Q(segment__isnull=True))
                ),
                name='formateur_type_segment_consistency'
            )
        ]



class Superviseur(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, null=True, blank=True)
    lignes = models.ManyToManyField(Ligne, related_name='superviseurs')

    def __str__(self):
        return f"{self.agent.prenom} {self.agent.nom} (Superviseur)"


class Personnel(models.Model):
    OPERATOR_STATE = 'Operateur'
    PERSONNEL_STATE = 'Candidat'
    EN_FORMATION_STATE = 'En Formation'
    STATE_CHOICES = [
        (OPERATOR_STATE, 'Operateur'),
        (PERSONNEL_STATE, 'Candidat'),
        (EN_FORMATION_STATE, 'En Formation')
    ]

    agent = models.OneToOneField(Agent, on_delete=models.CASCADE)
    etat = models.CharField(max_length=100, choices=STATE_CHOICES, default=PERSONNEL_STATE)
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE, null=True, blank=True)
    poste = models.ForeignKey('Poste', on_delete=models.CASCADE, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.etat == self.OPERATOR_STATE and not self.ligne and not self.poste:
            raise ValueError("Ligne and Poste must be set if the etat is Operator.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.agent.prenom} {self.agent.nom} ({self.agent.role})"

class Poste(models.Model):
    TYPE_CHOICES = [
        ('simple_sans_risque', 'Simple sans risque'),
        ('simple_avec_risque', 'Simple avec des risques'),
        ('compliqué_sans_risque', 'Compliqué sans risque'),
        ('compliqué_avec_risque', 'Compliqué avec le risque'),
    ]

    name = models.CharField(max_length=100)
    lignes = models.ManyToManyField(Ligne, related_name='postes')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='simple_sans_risque')

    def __str__(self):
        return self.name
class Polyvalence(models.Model):
    supervisor = models.ForeignKey(Superviseur, on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE)
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    comments = models.TextField()

    class Meta:
        unique_together = ('personnel', 'poste', 'ligne')

    def save(self, *args, **kwargs):
        if self.personnel.etat != Personnel.OPERATOR_STATE:
            raise ValueError("Personnel must be in 'Operateur' state to be rated.")
        if self.personnel.ligne not in self.supervisor.lignes.all():
            raise ValueError("Personnel must belong to the supervisor's line.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Polyvalence for {self.personnel} by {self.supervisor} in {self.poste} on {self.ligne}"


class Test(models.Model):
    type_test = models.CharField(max_length=100)
    date_test = models.DateField()
    responsables_ecole_formation = models.ManyToManyField('ResponsableEcoleFormation', related_name='tests')
    formateurs = models.ManyToManyField('Formateur', related_name='tests')
    note_test = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='tests')

    def __str__(self):
        responsables = ", ".join([str(r) for r in self.responsables_ecole_formation.all()])
        formateurs = ", ".join([str(f) for f in self.formateurs.all()])
        return (f"Test: {self.type_test} le {self.date_test} | Personnel: {self.personnel} | "
                f"Note: {self.note_test} | Responsables: {responsables} | Formateurs: {formateurs}")


class Contrat(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    type_contrat = models.CharField(max_length=100)
    date_creation_contrat = models.DateField()
    duree_contrat = models.IntegerField()

    def __str__(self):
        return f"Contrat de {self.agent.prenom} {self.agent.nom} ({self.type_contrat})"

class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
