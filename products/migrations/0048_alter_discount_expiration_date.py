# Generated by Django 4.1.4 on 2024-02-05 17:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0047_alter_discount_promo_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 15, 21, 27, 14, 532990)),
        ),
    ]