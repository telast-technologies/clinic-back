# Generated by Django 5.0.6 on 2024-05-18 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_is_client_admin"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_client_admin",
        ),
    ]
