# Generated by Django 3.0.3 on 2020-03-15 10:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plants',
            name='water_every',
            field=models.PositiveIntegerField(default=7, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(60)]),
        ),
    ]
