# Generated by Django 5.0.6 on 2024-05-18 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0002_staff_is_client_admin"),
        ("system_management", "0003_exposedpermission"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="permissions",
            field=models.ManyToManyField(related_name="staff", to="system_management.exposedpermission"),
        ),
    ]