# Generated by Django 4.1.13 on 2024-06-06 07:18

from django.db import migrations, models
import django.db.models.deletion


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
                ('email', models.EmailField(max_length=100, unique=True)),
                ('prenom', models.CharField(max_length=100)),
                ('nom', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('addresse', models.CharField(max_length=255)),
                ('cin', models.CharField(max_length=20, unique=True)),
                ('numerotel', models.CharField(max_length=20)),
                ('role', models.CharField(choices=[('RH', 'RH'), ('ResponsableFormation', 'Responsable Formation'), ('ResponsableEcoleFormation', 'Responsable Ecole Formation'), ('Formateur', 'Formateur'), ('Superviseur', 'Superviseur'), ('Personnel', 'Personnel')], default='Personnel', max_length=50)),
                ('username', models.CharField(max_length=100, null=True, unique=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_name='agent_groups', related_query_name='agent_group', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='agent_user_permissions', related_query_name='agent_user_permission', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ligne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Superviseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.agent')),
                ('ligne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ligne')),
            ],
        ),
        migrations.CreateModel(
            name='RH',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.agent')),
            ],
        ),
        migrations.CreateModel(
            name='ResponsableFormation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(blank=True, max_length=100, null=True)),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.agent')),
            ],
        ),
        migrations.CreateModel(
            name='ResponsableEcoleFormation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(blank=True, max_length=100, null=True)),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.agent')),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etat', models.CharField(blank=True, default='Candidate', max_length=100, null=True)),
                ('agent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.agent')),
            ],
        ),
        migrations.CreateModel(
            name='Formateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isAffecteur', models.BooleanField(default=False)),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.agent')),
            ],
        ),
    ]
