# Generated by Django 5.0.1 on 2024-04-29 11:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_publication_verif_rename_identifiant_chef_nom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='date_inscription',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 29, 13, 35, 45, 22747)),
        ),
    ]
