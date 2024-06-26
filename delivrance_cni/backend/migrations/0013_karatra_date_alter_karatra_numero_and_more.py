# Generated by Django 5.0.1 on 2024-05-15 12:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_alter_notification_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='karatra',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='karatra',
            name='numero',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateField(default=datetime.date(2024, 5, 15)),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='date_inscription',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 15, 14, 43, 29, 256842)),
        ),
    ]
