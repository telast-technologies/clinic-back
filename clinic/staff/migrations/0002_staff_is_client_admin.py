# Generated by Django 5.0.6 on 2024-05-18 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="is_client_admin",
            field=models.BooleanField(default=False),
        ),
    ]
