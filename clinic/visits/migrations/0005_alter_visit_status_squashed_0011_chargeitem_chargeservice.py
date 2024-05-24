# Generated by Django 5.0.6 on 2024-05-23 17:37

import django.core.validators
import django.db.models.deletion
import django_fsm
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("healthcare", "0001_initial"),
        ("inventory", "0005_supply_qrcode"),
        ("patients", "0002_patientreport"),
        ("visits", "0004_visit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visit",
            name="status",
            field=django_fsm.FSMField(
                choices=[
                    ("pending", "Pending"),
                    ("booked", "Booked"),
                    ("checked_in", "Checked In"),
                    ("checked_out", "Checked Out"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=20,
                protected=True,
            ),
        ),
        migrations.DeleteModel(
            name="Visit",
        ),
        migrations.CreateModel(
            name="Visit",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                (
                    "visit_type",
                    models.CharField(choices=[("scheduled", "Scheduled"), ("walk_in", "Walk In")], max_length=20),
                ),
                (
                    "status",
                    django_fsm.FSMField(
                        choices=[
                            ("booked", "Booked"),
                            ("checked_in", "Checked In"),
                            ("financially_cleared", "Financially Cleared"),
                            ("checked_out", "Checked Out"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="booked",
                        max_length=20,
                        protected=True,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="visits", to="patients.patient"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ChargeItem",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("quantity", models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ("supply", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="inventory.supply")),
                (
                    "visit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="charge_items", to="visits.visit"
                    ),
                ),
            ],
            options={
                "unique_together": {("visit", "supply")},
            },
        ),
        migrations.CreateModel(
            name="ChargeService",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("service", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="healthcare.service")),
                (
                    "visit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="charge_services", to="visits.visit"
                    ),
                ),
            ],
            options={
                "unique_together": {("visit", "service")},
            },
        ),
    ]
