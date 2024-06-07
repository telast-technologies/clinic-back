# Generated by Django 5.0.6 on 2024-06-07 00:25

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0001_initial'),
        ('inventory', '0005_supply_qrcode'),
        ('invoices', '0002_alter_invoice_sub_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeItem',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charge_items', to='invoices.invoice')),
                ('supply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charge_items', to='inventory.supply')),
            ],
            options={
                'ordering': ('-created_at',),
                'unique_together': {('invoice', 'supply')},
            },
        ),
        migrations.CreateModel(
            name='ChargeService',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charge_services', to='invoices.invoice')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charge_services', to='healthcare.service')),
            ],
            options={
                'ordering': ('-created_at',),
                'unique_together': {('invoice', 'service')},
            },
        ),
    ]