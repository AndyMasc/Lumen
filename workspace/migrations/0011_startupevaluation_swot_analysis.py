# Generated by Django 5.2.4 on 2025-07-20 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0010_startupevaluation_market_trends'),
    ]

    operations = [
        migrations.AddField(
            model_name='startupevaluation',
            name='swot_analysis',
            field=models.TextField(default=''),
        ),
    ]
