# Generated by Django 4.1.13 on 2024-06-21 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_module_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='image',
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
