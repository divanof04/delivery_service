# Generated by Django 5.1.7 on 2025-03-19 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parceltype',
            name='type_id',
        ),
    ]
