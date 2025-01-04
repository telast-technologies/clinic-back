# Generated by Django 5.0.6 on 2024-12-31 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0013_staff_staff_id'),
        ('system_management', '0014_clinic_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='permissions',
            field=models.ManyToManyField(blank=True, related_name='staff', to='system_management.exposedpermission'),
        ),
    ]