# Generated by Django 5.0.6 on 2024-12-29 09:43

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0015_patient_medical_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='medical_number',
            field=django_extensions.db.fields.RandomCharField(blank=True, editable=False, help_text='medical number', include_alpha=False, length=6, unique=True),
        ),
    ]