# Generated by Django 4.1.4 on 2023-11-23 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_alter_product_color_alter_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
    ]
