# Generated by Django 5.1.2 on 2025-01-06 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recpaper_app', '0008_project_log_user_uuid_alter_project_project_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_log',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]