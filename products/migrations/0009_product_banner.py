# Generated by Django 4.1.4 on 2023-10-17 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='banner',
            field=models.ImageField(default='product/bn3-1.webp', upload_to='product/'),
        ),
    ]
