# Generated by Django 5.0.6 on 2024-05-21 23:33

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("system_management", "0004_alter_clinic_options_alter_package_options"),
        ("visits", "0002_delete_timeslot"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "days",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("monday", "Monday"),
                                ("tuesday", "Tuesday"),
                                ("wednesday", "Wednesday"),
                                ("thursday", "Thursday"),
                                ("friday", "Friday"),
                                ("saturday", "Saturday"),
                                ("sunday", "Sunday"),
                            ],
                            max_length=10,
                        ),
                        size=7,
                    ),
                ),
                (
                    "clinic",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="time_slots",
                        to="system_management.clinic",
                    ),
                ),
            ],
        ),
    ]
