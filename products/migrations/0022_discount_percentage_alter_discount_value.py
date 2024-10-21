# Generated by Django 4.1.4 on 2023-11-05 12:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_rename_discount_status_discount_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=100), django.core.validators.MinValueValidator(limit_value=1)]),
        ),
        migrations.AlterField(
            model_name='discount',
            name='value',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]