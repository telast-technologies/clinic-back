# Generated by Django 5.0.6 on 2024-10-17 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0010_patient_channel_patient_nid'),
        ('system_management', '0008_alter_clinic_uid_alter_exposedpermission_uid_and_more_squashed_0012_alter_clinic_uid_alter_exposedpermission_uid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddConstraint(
            model_name='patient',
            constraint=models.UniqueConstraint(fields=('email',), name='unique_patient_email', nulls_distinct=True),
        ),
    ]
