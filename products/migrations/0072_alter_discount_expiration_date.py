# Generated by Django 4.2.11 on 2024-10-17 07:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0071_alter_discount_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 27, 0, 0, tzinfo=datetime.timezone.utc)),
        ),
    ]
