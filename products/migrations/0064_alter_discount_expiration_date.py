# Generated by Django 4.1.4 on 2024-02-29 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0063_alter_discount_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 10, 0, 0, tzinfo=datetime.timezone.utc)),
        ),
    ]
