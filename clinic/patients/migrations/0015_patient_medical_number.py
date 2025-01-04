# Generated by Django 5.0.6 on 2024-12-29 09:42

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0014_remove_patient_medical_number_patient_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='medical_number',
            field=django_extensions.db.fields.RandomCharField(blank=True, editable=False, help_text='medical number', include_alpha=False, length=6),
        ),
    ]