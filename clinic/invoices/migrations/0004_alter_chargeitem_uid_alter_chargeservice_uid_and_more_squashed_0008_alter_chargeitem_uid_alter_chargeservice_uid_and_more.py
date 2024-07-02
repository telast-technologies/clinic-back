# Generated by Django 5.0.6 on 2024-06-24 01:14

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_chargeitem_chargeservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargeitem',
            name='uid',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='chargeservice',
            name='uid',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='uid',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, primary_key=True, serialize=False),
        ),
    ]