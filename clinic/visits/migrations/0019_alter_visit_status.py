# Generated by Django 5.0.6 on 2024-06-22 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0018_alter_chargeservice_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='status',
            field=models.CharField(choices=[('booked', 'Booked'), ('checked_in', 'Checked In'), ('checked_out', 'Checked Out'), ('cancelled', 'Cancelled')], default='booked', max_length=20),
        ),
    ]
