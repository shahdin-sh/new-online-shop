# Generated by Django 4.2.11 on 2024-10-20 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0074_alter_product_quantity'),
        ('orders', '0019_rename_signal_order_canceled_signal_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'product')},
        ),
    ]
