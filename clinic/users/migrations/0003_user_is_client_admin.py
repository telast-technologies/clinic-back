# Generated by Django 5.0.6 on 2024-05-18 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_staff_clinic_remove_staff_user_delete_patient_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_client_admin",
            field=models.BooleanField(default=False),
        ),
    ]
