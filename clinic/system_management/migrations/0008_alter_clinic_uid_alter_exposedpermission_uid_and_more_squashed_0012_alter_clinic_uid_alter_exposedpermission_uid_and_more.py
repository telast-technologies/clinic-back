# Generated by Django 5.0.6 on 2024-06-24 01:09

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system_management', '0007_clinic_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='uid',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='exposedpermission',
            name='uid',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='package',
            name='uid',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, primary_key=True, serialize=False),
        ),
    ]
