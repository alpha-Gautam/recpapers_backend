# Generated by Django 5.1.2 on 2024-11-24 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0003_alter_mentor_created_alter_student_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
