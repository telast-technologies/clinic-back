# Generated by Django 5.0.6 on 2024-05-18 07:21

import django.db.models.deletion
import phonenumber_field.modelfields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Package",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("price", models.PositiveIntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Clinic",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("address", models.CharField(max_length=100)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region="EG"),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                (
                    "package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="clinics",
                        to="system_management.package",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
