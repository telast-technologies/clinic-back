# Generated by Django 5.0.6 on 2024-05-23 04:33

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("patients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientReport",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("document", models.FileField(upload_to="patients/reports")),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="reports", to="patients.patient"
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
    ]
