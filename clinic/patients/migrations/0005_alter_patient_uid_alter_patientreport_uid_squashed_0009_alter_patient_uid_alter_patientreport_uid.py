# Generated by Django 5.0.6 on 2024-06-24 01:12

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_alter_patientreport_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='uid',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='patientreport',
            name='uid',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, primary_key=True, serialize=False),
        ),
    ]
