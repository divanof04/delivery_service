# Generated by Django 5.1.7 on 2025-03-19 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParcelType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('type_id', models.PositiveIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('weight', models.FloatField()),
                ('content_cost', models.FloatField()),
                ('delivery_cost', models.FloatField(blank=True, null=True)),
                ('session_key', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parcel_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parcels.parceltype')),
            ],
        ),
    ]
