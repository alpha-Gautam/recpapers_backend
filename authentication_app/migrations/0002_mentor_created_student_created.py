# Generated by Django 5.1.2 on 2024-11-24 09:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 24, 14, 50, 57, 86564)),
        ),
        migrations.AddField(
            model_name='student',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 24, 14, 50, 57, 85191)),
        ),
    ]
