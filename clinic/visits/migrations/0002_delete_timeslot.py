# Generated by Django 5.0.6 on 2024-05-21 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("visits", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TimeSlot",
        ),
    ]