# Generated by Django 5.0.1 on 2024-04-29 14:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_utilisateur_date_inscription_retour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='date_inscription',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 29, 16, 21, 55, 57118)),
        ),
    ]
