# Generated by Django 4.1.4 on 2023-11-22 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_alter_discount_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='banner',
            field=models.ImageField(blank=True, default='product/bn3-1.webp', null=True, upload_to='product/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='product_default/shopping_kart.jpg', null=True, upload_to='product/'),
        ),
    ]
