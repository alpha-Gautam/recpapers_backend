# Generated by Django 5.1.2 on 2025-05-23 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recpaper_app', '0016_alter_project_github_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='semester',
            field=models.IntegerField(default=8),
            preserve_default=False,
        ),
    ]
