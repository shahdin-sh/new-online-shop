# Generated by Django 4.1.4 on 2023-02-20 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0036_remove_product_color_remove_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]