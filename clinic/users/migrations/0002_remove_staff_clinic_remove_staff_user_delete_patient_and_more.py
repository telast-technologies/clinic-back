# Generated by Django 5.0.6 on 2024-05-18 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="staff",
            name="clinic",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="user",
        ),
        migrations.DeleteModel(
            name="Patient",
        ),
        migrations.DeleteModel(
            name="Staff",
        ),
    ]