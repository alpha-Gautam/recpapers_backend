# Generated by Django 5.1.2 on 2024-12-28 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recpaper_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='project_log',
            name='project_id',
        ),
        migrations.AddField(
            model_name='keyword',
            name='project_uuid',
            field=models.CharField(default='asdfghjkl', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project_log',
            name='project_uuid',
            field=models.CharField(default='asdfghj', max_length=100),
            preserve_default=False,
        ),
    ]
