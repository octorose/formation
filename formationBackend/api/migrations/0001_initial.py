from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_email_verified', models.BooleanField(default=False)),
                ('prenom', models.CharField(max_length=100)),
                ('nom', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('addresse', models.CharField(max_length=255)),
                ('cin', models.CharField(max_length=20, unique=True)),
                ('numerotel', models.CharField(max_length=20)),
                ('role', models.CharField(choices=[('RH', 'RH'), ('ResponsableFormation', 'Responsable Formation'), ('ResponsableEcoleFormation', 'Responsable Ecole Formation'), ('Formateur', 'Formateur'), ('Superviseur', 'Superviseur'), ('Personnel', 'Personnel')], default='Personnel', max_length=50)),
                ('temporary_session', models.BooleanField(default=False)),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('site', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Formateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('type_contrat', models.CharField(max_length=100)),
                ('date_creation_contrat', models.DateField()),
                ('duree_contrat', models.IntegerField()),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ligne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etat', models.CharField(choices=[('Operateur', 'Operateur'), ('Candidat', 'Candidat'), ('En Formation', 'En Formation')], default='Candidat', max_length=100)),
                ('agent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ligne', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ligne')),
            ],
        ),
        migrations.CreateModel(
            name='ResponsableEcoleFormation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_test', models.CharField(max_length=100)),
                ('date_test', models.DateField()),
                ('noteTest', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('formateurs', models.ManyToManyField(related_name='tests', to='api.formateur')),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='api.personnel')),
                ('responsables_ecole_formation', models.ManyToManyField(related_name='tests', to='api.responsableecoleformation')),
            ],
        ),
        migrations.CreateModel(
            name='Superviseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lignes', models.ManyToManyField(related_name='superviseurs', to='api.ligne')),
            ],
        ),
        migrations.CreateModel(
            name='RH',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResponsableFormation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(blank=True, max_length=100, null=True)),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('simple_sans_risque', 'Simple sans risque'), ('simple_avec_risque', 'Simple avec des risques'), ('compliqué_sans_risque', 'Compliqué sans risque'), ('compliqué_avec_risque', 'Compliqué avec le risque')], default='simple_sans_risque', max_length=50)),
                ('lignes', models.ManyToManyField(related_name='postes', to='api.ligne')),
            ],
        ),
        migrations.AddField(
            model_name='personnel',
            name='poste',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.poste'),
        ),
        migrations.AddField(
            model_name='ligne',
            name='superviseur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.superviseur'),
        ),
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('type_test', models.CharField(max_length=100)),
                ('date_test', models.DateField()),
                ('note_test', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('formateurs', models.ManyToManyField(related_name='tests', to='api.formateur')),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='api.personnel')),
                ('responsables_ecole_formation', models.ManyToManyField(related_name='tests', to='api.responsableecoleformation')),

            ],
        ),
        migrations.CreateModel(
            name='Polyvalence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('comments', models.TextField()),
                ('ligne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ligne')),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.personnel')),
                ('poste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.poste')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.superviseur')),
            ],
            options={
                'unique_together': {('personnel', 'poste', 'ligne')},
            },
        ),
    ]
