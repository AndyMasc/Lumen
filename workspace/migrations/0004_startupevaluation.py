# Generated by Django 5.2.4 on 2025-07-13 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0003_rename_startup_startupidea'),
    ]

    operations = [
        migrations.CreateModel(
            name='startupEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overview', models.TextField()),
                ('startupIdea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.startupidea')),
            ],
        ),
    ]
