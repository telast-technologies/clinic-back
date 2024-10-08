# Generated by Django 5.0.6 on 2024-05-18 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("approvals", "0002_alter_joinrequest_package"),
    ]

    operations = [
        migrations.AlterField(
            model_name="joinrequest",
            name="status",
            field=models.CharField(
                choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
                default="pending",
                max_length=100,
            ),
        ),
    ]
