# Generated by Django 5.2.4 on 2025-07-20 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0012_startupevaluation_overall_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='startupevaluation',
            name='areas_for_improvement',
            field=models.TextField(default=''),
        ),
    ]
