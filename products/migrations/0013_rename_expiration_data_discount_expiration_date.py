# Generated by Django 4.1.4 on 2023-10-25 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_discount_product_discounts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount',
            old_name='expiration_data',
            new_name='expiration_date',
        ),
    ]
