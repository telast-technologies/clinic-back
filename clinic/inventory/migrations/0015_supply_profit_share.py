# Generated by Django 5.0.6 on 2025-01-15 08:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_alter_supply_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='supply',
            name='profit_share',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
