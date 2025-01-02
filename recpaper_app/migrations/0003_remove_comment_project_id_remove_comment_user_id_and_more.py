# Generated by Django 5.1.2 on 2024-12-28 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recpaper_app', '0002_remove_keyword_project_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='platform',
            name='project_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='project_uuid',
            field=models.CharField(default='qwertyu', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='user_uuid',
            field=models.CharField(default='qwert', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='platform',
            name='project_uuid',
            field=models.CharField(default='qwertyu', max_length=100),
            preserve_default=False,
        ),
    ]