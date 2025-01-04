# Generated by Django 5.0.6 on 2024-12-29 10:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_management', '0008_alter_clinic_uid_alter_exposedpermission_uid_and_more_squashed_0012_alter_clinic_uid_alter_exposedpermission_uid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='profit_share',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Clinic Profit Share'),
        ),
    ]